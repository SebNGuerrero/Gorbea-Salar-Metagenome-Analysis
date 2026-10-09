import os
import subprocess

# Configuración
TRIMMED_DIR = "/media/colivos/Elements/Metagenomas_Gorbea/fastp"
DECON_DIR = "/media/colivos/Elements/Metagenomas_Gorbea/Decon"
GRCH38_INDEX = "/media/colivos/Elements/GRCh38_index/GRCh38"
THREADS_BWA = 10
THREADS_SAM = 6

SAMPLES = ["T6", "T7", "T8"]



def align_to_grch38(sample):
    r1 = f"{TRIMMED_DIR}/{sample}_trimmed_R1.fastq.gz"
    r2 = f"{TRIMMED_DIR}/{sample}_trimmed_R2.fastq.gz"
    bam_out = f"{DECON_DIR}/{sample}_GRCh38.bam"
    
    cmd = (f"bwa-mem2 mem -t {THREADS_BWA} {GRCH38_INDEX} {r1} {r2} | "
           f"samtools view -@ {THREADS_SAM} -b -o {bam_out} -")
    subprocess.run(cmd, shell=True)

# Verifica si el archivo bam_out existe después de la ejecución del comando. Si no existe
# probablemente hubo un error y en el main se interrumpe el pipeline. return 1 y se sale del main.
    
    if os.path.exists(bam_out):
        return True
    else:
        return False

def get_flagstat(sample):
    bam = f"{DECON_DIR}/{sample}_GRCh38.bam"
    flagstat_out = f"{DECON_DIR}/{sample}_GRCh38_flagstat.txt"
    
    cmd = f"samtools flagstat -@ {THREADS_SAM} {bam} > {flagstat_out}"
    subprocess.run(cmd, shell=True)

    # Verifica si el archivo flagstat_out existe después de la ejecución del comando. 

    if os.path.exists(flagstat_out):
        return True
    else:
        return False

def extract_unmapped(sample):
    bam = f"{DECON_DIR}/{sample}_GRCh38.bam"
    filtered_1 = f"{DECON_DIR}/{sample}_filtered_1.fastq.gz"
    filtered_2 = f"{DECON_DIR}/{sample}_filtered_2.fastq.gz"
    
    cmd = (f"samtools view -@ {THREADS_SAM} -b -e 'flag & 4 || flag & 8' -F 2304 {bam} | "
           f"samtools collate -u -@ {THREADS_SAM} -O - | "
           f"samtools fastq -1 {filtered_1} "
           f"-2 {filtered_2} "
           f"-0 /dev/null -s /dev/null -")
    subprocess.run(cmd, shell=True)

    # Verifica si el archivo filtered_1 y filtered_2 existen después de la ejecución del comando. 
    
    if os.path.exists(filtered_1) and os.path.exists(filtered_2):
        return True
    else:
        return False

def main():
    os.makedirs(DECON_DIR, exist_ok=True)
    
    for sample in SAMPLES:
        print(f"\n{'#'*60}")
        print(f"# {sample}")
        print(f"{'#'*60}")
        
        if not align_to_grch38(sample):
            print(f"ERROR: Fallo align_to_grch38 en {sample}")
            return 1
        if not get_flagstat(sample):
            print(f"ERROR: Fallo get_flagstat en {sample}")
            return 1
        if not extract_unmapped(sample):
            print(f"ERROR: Fallo extract_unmapped en {sample}")
            return 1

if __name__ == "__main__":
    main()