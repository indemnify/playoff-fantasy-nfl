import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import os
import shutil
from run_pipeline import NFLPipeline, PipelineError

class TestNFLPipeline(unittest.TestCase):
    def setUp(self):
        # Create test directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Create test data files
        with open('data/stats.csv', 'w') as f:
            f.write('test,data\n1,2\n')
        
        self.pipeline = NFLPipeline()
    
    def tearDown(self):
        # Clean up test files and directories
        for dir_name in ['logs', 'backups', 'data']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
    
    def test_backup_data(self):
        """Test backup functionality"""
        backup_dir = self.pipeline._backup_data()
        self.assertTrue(os.path.exists(backup_dir))
        self.assertTrue(os.path.exists(os.path.join(backup_dir, 'stats.csv')))
    
    @patch('data_import.nfl_stats_import.NFLStatsImporter.run_import')
    def test_run_stats_import_success(self, mock_import):
        """Test successful stats import"""
        mock_import.return_value = True
        result = self.pipeline.run_stats_import()
        
        self.assertTrue(result['success'])
        self.assertIn('backup_dir', result)
        self.assertIn('timestamp', result)
    
    @patch('data_import.nfl_stats_import.NFLStatsImporter.run_import')
    def test_run_stats_import_failure(self, mock_import):
        """Test failed stats import"""
        mock_import.return_value = False
        result = self.pipeline.run_stats_import()
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    @patch('data_import.playoff_roster_generator.PlayoffRosterGenerator.run_full_update')
    def test_run_roster_generator_success(self, mock_update):
        """Test successful roster generation"""
        mock_update.return_value = None  # Successful execution
        result = self.pipeline.run_roster_generator()
        
        self.assertTrue(result['success'])
        self.assertIn('timestamp', result)
    
    @patch('data_import.playoff_roster_generator.PlayoffRosterGenerator.run_full_update')
    def test_run_roster_generator_failure(self, mock_update):
        """Test failed roster generation"""
        mock_update.side_effect = Exception('Test error')
        result = self.pipeline.run_roster_generator()
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_execute_pipeline_full_success(self):
        """Test successful complete pipeline execution"""
        with patch('run_pipeline.NFLPipeline.run_stats_import') as mock_stats,\
             patch('run_pipeline.NFLPipeline.run_roster_generator') as mock_roster:
            
            mock_stats.return_value = {'success': True, 'backup_dir': 'test_backup'}
            mock_roster.return_value = {'success': True}
            
            results = self.pipeline.execute_pipeline()
            
            self.assertTrue(results['success'])
            self.assertIn('duration', results)
            self.assertEqual(len(results['errors']), 0)
    
    def test_execute_pipeline_stats_failure(self):
        """Test pipeline execution with stats import failure"""
        with patch('run_pipeline.NFLPipeline.run_stats_import') as mock_stats:
            mock_stats.return_value = {'success': False, 'error': 'Test error'}
            
            results = self.pipeline.execute_pipeline()
            
            self.assertFalse(results['success'])
            self.assertTrue(len(results['errors']) > 0)
    
    def test_pipeline_logging(self):
        """Test pipeline logging functionality"""
        self.pipeline.logger.info('Test log message')
        
        log_file = os.path.join('logs', 'pipeline.log')
        self.assertTrue(os.path.exists(log_file))
        
        with open(log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('Test log message', log_content)

if __name__ == '__main__':
    unittest.main()