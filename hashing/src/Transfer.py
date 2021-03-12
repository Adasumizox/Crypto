import requests
import sys


class Transfer:
    @staticmethod
    def download_file(url: str) -> str:

        assert len(url) > 0

        filename = url.split('/')[-1]

        with open(filename, 'wb') as output_file:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                output_file.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    output_file.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')

        return filename
