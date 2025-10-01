# main.py

from extractor.map_reader import H3MParser

if __name__ == "__main__":
    file_path = "maps/[HotA] A Cold Day in Hell.h3m"
    parser = H3MParser(file_path)
    parser.parse()
    print(parser.to_json())
