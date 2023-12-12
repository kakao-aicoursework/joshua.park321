
import chromadb

def data_카카오싱크():
    filename = '../data/project_data_카카오싱크.txt'

    with open(filename) as f:
        lines = f.readlines()

    return lines
