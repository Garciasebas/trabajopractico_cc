# This is a sample Python script.
import tabula
import os
from csv import reader
from pathlib import Path

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Persona:
    def __init__(self, ci, nombre, monto):
        self.ci = ci
        self.nombre = nombre
        self.monto = monto

def leer_csv(nombre_archivo):
    with open('./tabula-csv-out/' + nombre_archivo + '.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            list_persona = []
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                # print(row)
                if(row[0] == ""):
                    cinombre = row[1].split(" ",1)
                    monto = row[4].split(" ",1)[0]
                    persona = Persona(cinombre[0], cinombre[1], monto)
                else:
                    cinombre = row[0].split(" ", 1)
                    monto = row[3].split(" ", 1)[0]
                    persona = Persona(cinombre[0], cinombre[1], monto)
                list_persona.append(persona)
            convert(list_persona, './csv-final/' + nombre_archivo + '.csv')

def convert(list_persona, outfile):
    with open(outfile, 'w') as f:
        f.write('Ci;Nombre;Monto')
        f.write('\n')
        for persona in list_persona:
            f.write(persona.ci + ';' + persona.nombre + ';' + persona.monto)
            f.write('\n')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    files = os.listdir('./pdfs')
    for nombre_archivo in files:
        nombre_pdf = nombre_archivo.split('.')[0]
        nombre_carpeta_pdf_parts = './pdf-parts/' + nombre_pdf
        nombre_carpeta_jpeg = './jpeg/' + nombre_pdf
        nombre_carpeta_jpeg_pdf = './jpeg-pdf/' + nombre_pdf
        nombre_carpeta_pdf_searchable = './pdf-searchable/' + nombre_pdf
        nombre_carpeta_tabula_csv_out = './tabula-csv-out/' + nombre_pdf
        nombre_carpeta_csv_final = './csv-final/' + nombre_pdf
        Path(nombre_carpeta_pdf_parts).mkdir(parents=True, exist_ok=True)
        Path(nombre_carpeta_jpeg).mkdir(parents=True, exist_ok=True)
        Path(nombre_carpeta_jpeg_pdf).mkdir(parents=True, exist_ok=True)
        Path(nombre_carpeta_pdf_searchable).mkdir(parents=True, exist_ok=True)
        Path(nombre_carpeta_tabula_csv_out).mkdir(parents=True, exist_ok=True)
        Path(nombre_carpeta_csv_final).mkdir(parents=True, exist_ok=True)
        os.system('pdfseparate ./pdfs/' + nombre_pdf + '.pdf ' + nombre_carpeta_pdf_parts + '/part-%d')
        files = os.listdir(nombre_carpeta_pdf_parts)
        for f in files:
            print(f)
            print('pdftoppm')
            os.system('pdftoppm -singlefile -jpeg -r 600 -jpegopt quality=100 ' + nombre_carpeta_pdf_parts + '/' + f + ' ' + nombre_carpeta_jpeg + '/' + f)
            print('img2pdf')
            os.system('img2pdf ' + nombre_carpeta_jpeg + '/' + f + '.jpg -o ' + nombre_carpeta_jpeg_pdf + '/' + f + '-jpeg.pdf')
            print('ocrmypdf')
            os.system('ocrmypdf -f --tesseract-pagesegmode 6 --jpeg-quality 100 ' + nombre_carpeta_jpeg_pdf + '/' + f + '-jpeg.pdf ' + nombre_carpeta_pdf_searchable + '/' + f + '-jpeg-ocr.pdf -l spa')
            print('tabula')
            tabula.convert_into(nombre_carpeta_pdf_searchable + "/" + f + "-jpeg-ocr.pdf", nombre_carpeta_tabula_csv_out + "/" + f + ".csv", output_format="csv", pages='all')
            print('final')
            leer_csv(nombre_pdf + '/' + f)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
