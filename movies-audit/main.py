import logging
import db_model


log = logging.getLogger('movies-audit')


if __name__ == '__main__':
    log.info(f'Starting movies audit...')

    movies_audit = db_model.MoviesAudit()
    movies_audit.audit()
    movies_audit.save_result()

    log.info(f'Finished audit.\nResults can be found in {movies_audit.result_file} file.')