files = {'file': (f'{objectName}', new_csv, 'text/csv')}
        response = requests.post(f'{upload_endpoint}/putObject/{bucketName}/{objectName}', files=files)
        if response.status_code == 200:
            logging.info(f'Upload complete: {response}')
        else:
            raise Exception("Failed to upload new csv to s3")