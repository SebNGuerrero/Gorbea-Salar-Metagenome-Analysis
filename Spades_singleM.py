import os
import subprocess
import sys
 
SAMPLES = ['T6']
 
BASE_DIR = '/media/colivos/Elements/Metagenomas_Gorbea'
DECON_DIR = f'{BASE_DIR}/Decon'
SINGLEM_DIR = f'{BASE_DIR}/SingleM'
METASPADES_DIR = f'{BASE_DIR}/MetaSpades'
 
# Crear directorios si no existen
os.makedirs(SINGLEM_DIR, exist_ok=True)
os.makedirs(METASPADES_DIR, exist_ok=True)
 
os.environ['SINGLEM_METAPACKAGE_PATH'] = '/media/databases/singleM_data/S6.5.0.GTDB_r232.metapackage_20260319.smpkg'
 
print("Verificando variable de entorno...\n")
if not os.environ.get('SINGLEM_METAPACKAGE_PATH'):
    print("SINGLEM_METAPACKAGE_PATH no está definida\n")
    sys.exit(1)
 
print(f"SINGLEM_METAPACKAGE_PATH={os.environ['SINGLEM_METAPACKAGE_PATH']}\n")
 
if not os.path.exists(os.environ['SINGLEM_METAPACKAGE_PATH']):
    print(f"No existe: {os.environ['SINGLEM_METAPACKAGE_PATH']}\n")
    sys.exit(1)
 
print(f"Archivo existe\n")
 
print("Verificando integridad de base de datos SingleM...\n")
result = subprocess.run(['singlem', 'data', '--verify-only'])
if result.returncode != 0:
    print("Base de datos no es válida\n")
    sys.exit(1)
 
print("Base de datos OK\n")
 
print("Verificando recursos disponibles...\n")
result = subprocess.run(['free', '-h'], capture_output=True, text=True)
print(result.stdout)
 
result = subprocess.run(['nproc'], capture_output=True, text=True)
num_cores = int(result.stdout.strip())
print(f"Número de procesadores disponibles: {num_cores}\n")
 
print("NOTA: metaSPAdes usa -t 10 threads y -m 200 GB de memoria\n")
 
for SAMPLE in SAMPLES:
    print(f"\n{'='*50}")
    print(f"Procesando {SAMPLE}")
    print(f"{'='*50}\n")
    
    # SingleM
    print(f"[1] Ejecutando SingleM...")
    r1 = f'{DECON_DIR}/{SAMPLE}_filtered_1.fastq.gz'
    r2 = f'{DECON_DIR}/{SAMPLE}_filtered_2.fastq.gz'
    profile = f'{SINGLEM_DIR}/{SAMPLE}_singlem_profile.tsv'
    otu = f'{SINGLEM_DIR}/{SAMPLE}_singlem_otu.tsv'
    
    subprocess.run(['singlem', 'pipe', '-1', r1, '-2', r2, '-p', profile, '--otu-table', otu, '--threads', '8'])
    
    if os.path.exists(profile) and os.path.exists(otu):
        print(f"SingleM OK\n")
    else:
        print(f"SingleM FALLÓ\n")
        sys.exit(1)
    
    # metaSPAdes
    print(f"[2] Ejecutando metaSPAdes...")
    out = f'{METASPADES_DIR}/{SAMPLE}_metaspades'
    log = f'{METASPADES_DIR}/{SAMPLE}_metaspades.log'
    
    subprocess.run(f'spades.py --meta -1 {r1} -2 {r2} -t 10 -m 200 -o {out} > {log} 2>&1', shell=True)
    
    if os.path.exists(f'{out}/contigs.fasta'):
        print(f"metaSPAdes OK\n")
    else:
        print(f"metaSPAdes FALLÓ\n")
        sys.exit(1)
    
    print(f"{SAMPLE} completado\n")
 
print(f"{'='*50}")
print("Pipeline completado")
print(f"{'='*50}")
