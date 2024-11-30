import logging
import os
import sys
import time
from datetime import datetime
from typing import Optional, Dict, Any
from data_import.nfl_stats_import import NFLStatsImporter
from data_import.playoff_roster_generator import PlayoffRosterGenerator

class PipelineError(Exception):
    """Custom exception for pipeline errors"""
    pass

class NFLPipeline:
    def __init__(self):
        self._setup_logging()
        self.stats_importer = NFLStatsImporter()
        self.roster_generator = PlayoffRosterGenerator()
        self.last_run = None
        self.errors = []
    
    def _setup_logging(self):
        """Configure logging for the pipeline"""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Setup file handler
        log_file = os.path.join('logs', 'pipeline.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        # Setup console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        
        # Configure logger
        self.logger = logging.getLogger('NFLPipeline')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _backup_data(self):
        """Create backup of current data"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join('backups', timestamp)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup relevant data files
            data_files = ['data/stats.csv', 'data/rosters.csv']
            for file in data_files:
                if os.path.exists(file):
                    backup_file = os.path.join(backup_dir, os.path.basename(file))
                    with open(file, 'r') as src, open(backup_file, 'w') as dst:
                        dst.write(src.read())
            
            self.logger.info(f'Backup created in {backup_dir}')
            return backup_dir
        except Exception as e:
            self.logger.error(f'Backup failed: {str(e)}')
            raise PipelineError(f'Backup failed: {str(e)}')
    
    def run_stats_import(self) -> Dict[str, Any]:
        """Run the NFL stats import process"""
        self.logger.info('Starting stats import process')
        try:
            # Create backup before import
            backup_dir = self._backup_data()
            
            # Run import
            stats_result = self.stats_importer.run_import()
            
            if not stats_result:
                raise PipelineError('Stats import failed')
            
            self.logger.info('Stats import completed successfully')
            return {
                'success': True,
                'backup_dir': backup_dir,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f'Stats import failed: {str(e)}')
            self.errors.append({
                'step': 'stats_import',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {'success': False, 'error': str(e)}
    
    def run_roster_generator(self) -> Dict[str, Any]:
        """Run the playoff roster generator process"""
        self.logger.info('Starting roster generation process')
        try:
            # Run roster generation
            self.roster_generator.run_full_update()
            
            self.logger.info('Roster generation completed successfully')
            return {
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f'Roster generation failed: {str(e)}')
            self.errors.append({
                'step': 'roster_generator',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return {'success': False, 'error': str(e)}
    
    def execute_pipeline(self) -> Dict[str, Any]:
        """Execute the complete pipeline"""
        start_time = time.time()
        self.logger.info('Starting pipeline execution')
        
        # Track results
        results = {
            'stats_import': None,
            'roster_generator': None,
            'success': False,
            'errors': [],
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # Run stats import
            results['stats_import'] = self.run_stats_import()
            if not results['stats_import']['success']:
                raise PipelineError('Stats import step failed')
            
            # Run roster generator
            results['roster_generator'] = self.run_roster_generator()
            if not results['roster_generator']['success']:
                raise PipelineError('Roster generator step failed')
            
            # Update results
            results['success'] = True
            results['duration'] = time.time() - start_time
            results['end_time'] = datetime.now().isoformat()
            
            self.last_run = datetime.now()
            self.logger.info('Pipeline completed successfully')
            
        except Exception as e:
            self.logger.error(f'Pipeline failed: {str(e)}')
            results['success'] = False
            results['errors'] = self.errors
            results['duration'] = time.time() - start_time
            results['end_time'] = datetime.now().isoformat()
        
        return results

def main():
    pipeline = NFLPipeline()
    results = pipeline.execute_pipeline()
    
    if results['success']:
        print('Pipeline completed successfully')
        print(f'Duration: {results["duration"]:.2f} seconds')
    else:
        print('Pipeline failed')
        print('Errors:')
        for error in results['errors']:
            print(f"- {error['step']}: {error['error']}")
        sys.exit(1)

if __name__ == '__main__':
    main()