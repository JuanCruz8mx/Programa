import json
cedis={
    "metropolitano en azcapotzalco":"ciudad de mexico",
    "tijuana":"baja california",
    "mexicali":"baja california",
    "hermosillo":"sonora",
    "cd juarez/cd obregon":"sonora",
    "monterrey":"nuevo leon",
    "saltillo":"coahuila",
    "torreon":"coahuila",
    "reyona":"tamaulipas",
    "matamoros":"tamaulipas",
    "cd victoria":"tamaulipas",
    "altamira":"tamaulipas",
    "ciudad mante":"tamaulipas",
    "guadalajara":"jalisco",
    "leon":"guanajuato",
    "aguas calientes":"aguas calientes",
    "colima":"colima",
    "morelia":"michoacan",
    "puebla":"puebla",
    "queretaro":"queretaro",
    "pachuca":"hidalgo",
    "toluca":"estado de mexico",
    "cuernavaca":"morelos",
    "ciudad de mexico":"CDMX",
    "acapulco":"guerrero",
    "chipalcingo":"guerrero",
    "oaxaca":"oaxaca",
    "tapachula":"chiapas",
    "veracruz":"veracruz",
    "villa hermosa":"tabasco",
    "coatzacoalcos":"veracruz",
    "merida":"yucatan",
    "cancun":"quintana roo",
    "chetumal":"quintana roo"

    

}

nombre_de_archivo="centros.json"
try:
    with open(nombre_de_archivo,'w', encoding='utf-8') as archivo_json:
        json.dump(cedis, archivo_json, indent=4, ensure_ascii=False)
        print(f"'{nombre_de_archivo}' creado exitosamente.")
except IOError as e:
    print(f'error al escribir en el archivo: {e}')