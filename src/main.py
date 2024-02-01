import os
import sys
import threading

from downloaders.NCBI.ncbi_downloader import NCBI_Downloader
from downloaders.FungiDB.fungidb_downloader import FungiDB_Downloader
from downloaders.EnsemblFungi.ensembl_download import EnsemblFungi_Downloader
from downloaders.MycoCosm.mycocosm_download import MycoCosm_Downloader
from utils.merger import merge_dbs, merge_gffs
from utils.gff_to_cds import create_cds_from_gff


def initialize_downloader(downloader_class):
    downloader = downloader_class()
    downloader.download()


def main(choice_arg=''):
    if not os.path.exists('data'):
        os.mkdir('data')

    choice = '0'

    downloaders = {
        '1': NCBI_Downloader,
        '2': FungiDB_Downloader,
        '3': EnsemblFungi_Downloader,
        '4': MycoCosm_Downloader,
    }

    if choice_arg:
        print(f'Received choice {choice_arg} via argv.')
        choice = choice_arg
    else:
        print('Welcome to FUGUE. Select an option:\n')
        choice = input('1. NCBI Datasets\n2. FungiDB\n3. EnsemblFungi\n4. MycoCosm\n5. Create CDS from GFF\n6. Merge Downloads\n7. Merge GFF\n8. All of the Above\n9. Quit\nYour choice: ')

    if choice in downloaders:
        downloader = downloaders[choice]()
        downloader.download()

    elif choice == '5':
        create_cds_from_gff()

    elif choice == '6':
        merge_dbs()

    elif choice == '7':
        merge_gffs()

    elif choice == '8':
        threads = []
        for _, downloader_class in downloaders.items():
            thread = threading.Thread(target=initialize_downloader, args=(downloader_class,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print('Merging...')
        merge_dbs()
        print('Creating CDS from GFF...')
        create_cds_from_gff()
        print('Merging GFFs...')
        merge_gffs()

    print('Goodbye.')
    return 0
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(main(sys.argv[1]))
    sys.exit(main())