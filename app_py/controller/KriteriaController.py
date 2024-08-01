from app_py import app, db, response
from flask import Flask, jsonify, request
from app_py.model.KriteriaModel import Kriteria, db
import numpy as np
from fractions import Fraction as fr
from app_py.model.LaptopModel import Laptop
from sqlalchemy.sql import func

CR = 0

nilai_cpu = []
nilai_gpu = []
nilai_storage = []
nilai_display = []
nilai_ram = []
nilai_price = []
nilai_name = []

result = []
values = []

name = ''

def tampil_kriteria():
    try:
        kriteria = Kriteria.query.all()
        result = []
        for i in kriteria:
            result.append(
                {
                 'id': i.id,
                 'name': i.name_kriteria,
                }
            )    
        return jsonify(result)
    
    except Exception as e:
        print(e)

def tampil_kriteria_by_id(id):
    try:
        kriteria = Kriteria.query.get(id)
        if kriteria:
            return jsonify({
                'id': kriteria.id,
                'name': kriteria.name_kriteria,
            })
        
        else:
            return jsonify({'error': 'Kriteria tidak ditemukan'})
    except Exception as e:
        print(e)


def simpan_kriteria():
    try:
        data = request.get_json()
        nameKriteria = data.get('name_kriteria')
        
        kriteria = Kriteria(name_kriteria = nameKriteria)
        db.session.add(kriteria)
        db.session.commit()

        return response.success('', 'Sukses menambah data')
        
    except Exception as e:
        print(e)

def edit_kriteria(id):
    kriteria = Kriteria.query.get(id)
    if kriteria:
        data = request.get_json()
        nameKriteria = data.get('name_kriteria') 
        
        kriteria.name_kriteria = nameKriteria
        db.session.commit()
            
        return response.success('', 'Sukses UPDATE data')

    else: 
        return jsonify({'message': 'Kriteria tidak ditemukan'})

def hapus_kriteria(id):
    kriteria = Kriteria.query.get(id)
    if kriteria:
        db.session.delete(kriteria)
        db.session.commit()
        return jsonify({'message': 'Data kriteria berhasil dihapus'})
    else:
        return jsonify({'message': 'Kriteria tidak ditemukan'})
    
def hitung_kriteria():
    try:
        def bobot(val):
            normalized_matrix = val / val.sum(axis=0)
            # print(f'normalized matrix \n{normalized_matrix}')
            weights = normalized_matrix.mean(axis=1)
            return weights
        
        data = request.json
        print(f'\n{data}')

        # Extracting values from the input data and ensuring they are in the correct format
        kriteria = list(data.values())
        # kriteria = list(data['kriteria'].values())
        # laptops = data['laptops']

        n = len(kriteria)
        print(f"Number of criteria: {n}")
        print(f"kriteria awal {kriteria}\n")

        n_nilai = len(nilai_price)
        # print(n_nilai)
        
        kriteria_matrix = matrix(n, kriteria)
        kriteria_weights = bobot(kriteria_matrix)
        # total = kriteria_matrix.sum(axis=0)

        # Consistency check
        # lambda_max = np.dot(pairwise_matrix, weights).sum() / weights.sum()
        lambda_max = np.dot(kriteria_matrix, kriteria_weights).sum() / kriteria_weights.sum()
        CI = (lambda_max - n) / (n - 1)
        RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]
        CR_temp = CI / RI[n - 1]
        CR = round(CR_temp, 3)

        # criteria_names = list(data['kriteria'].keys())
        # criteria_values = {name: [] for name in criteria_names}

        # for laptop in laptops:
        #     for name in criteria_names:
        #         criteria_values[name].append(laptop[name])

        # criteria_weights = {}
        # for name in criteria_names:
        #     criteria_matrix = matrix(len(criteria_values[name]), criteria_values[name])
        #     criteria_weights[name] = bobot(criteria_matrix)

        kriteria_price = matrix(n_nilai, nilai_price)
        kriteria_cpu = matrix(n_nilai, nilai_cpu)
        kriteria_ram = matrix(n_nilai, nilai_ram)
        kriteria_storage = matrix(n_nilai, nilai_storage)

        price = bobot(kriteria_price)
        cpu = bobot(kriteria_cpu)
        ram = bobot(kriteria_ram)
        storage = bobot(kriteria_storage)

        # Menghitung skor total untuk setiap laptop
        scores = []
        # print(f"jml laptop (nilai cpu) {len(nilai_cpu)}\n")

        # for i in range(len(laptops)):
        #     total_score = sum(
        #         kriteria_weights[j] * criteria_weights[name][i]
        #         for j, name in enumerate(criteria_names)
        #     )
        #     scores.append(total_score)
        
        for i in range(len(nilai_price)):
            total_score = (
                           kriteria_weights[0] * price[i] +
                           kriteria_weights[1] * cpu[i] +
                           kriteria_weights[2] * ram[i] +
                           kriteria_weights[3] * storage[i]
                           )
            scores.append(total_score)

        print(f'kriteria matrix\n{kriteria_matrix}\n')
        # print(f'total matrix {total}\n')
        print(f'kriteria weights/bobot normal\n{kriteria_weights}\n')
        
        print(f"lambda max {lambda_max}")
        print(f"ci {CI}")
        print(f"cr {CR}\n")
        
        print(f"jml laptop (scores) {len(scores)}\n")
        print(scores)
        # print(f"score {scores}\n")

        # Mengurutkan laptop berdasarkan skor total dan mengambil 10 laptop teratas
        top_laptops_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:10]
        top_laptops = [result[i] for i in top_laptops_indices]

        print(f"indices laptop {top_laptops_indices}\n")
        # print(f"laptop paling bagus {top_laptops}")

        response = {
            "CR": CR,
            "top_laptop": top_laptops,
        }

        # print(f"Response: {response}")
        print("")

        return jsonify(response)
    except Exception as e:
        print(f"Error in hitung_kriteria: {e}")  # Debugging: Print any errors that occur
        return jsonify({"Error": str(e)}), 400
    
def matrix(n, criteria):
    try:
        criteria = [float(c) for c in criteria]
        pairwise_matrix = np.zeros((n, n), dtype=object)

        for i in range(n):
            for j in range(n):
                cri = criteria[i]
                crj = criteria[j-1]
                if i == j:
                    pairwise_matrix[i][j] = 1.0
                # elif i == 0 or i == 1:
                # elif i == 0:
                #     pairwise_matrix[i][j] = float(criteria[j])
                #     print(f'index {[i]},{[j]} = {pairwise_matrix[i][j]}')
                #     pairwise_matrix[j][i] = 1 / pairwise_matrix[i][j]
                elif i < j:
                    pairwise_matrix[i][j] = float(crj/criteria[j])
                    # print(f'index {[i]},{[j]} = {float(crj)}/{float(criteria[j])} = {pairwise_matrix[i][j]}')
                    # pairwise_matrix[i][j] = float(pairwise_matrix[i-1][j-1]/pairwise_matrix[i-1][j])
                    pairwise_matrix[j][i] = 1 / pairwise_matrix[i][j]

        # print(f'matrix\n{pairwise_matrix}\n')
        return pairwise_matrix
    except Exception as e:
        print(f'error in matrix: {e}')
        return jsonify({"error": str(e)}), 400

def val_cpu(proc):
    cpu_mapping = {
        'celeron': 1,
        'pentium': 2,
        'athlon': 2,
        'dual core': 2,
        'r3': 4,
        'ryzen 3': 4,
        'i3': 4,
        'core 3': 4,
        'r5': 5,
        'ryzen 5': 5,
        'i5': 5,
        'ultra 5': 5,
        'm2': 5,
        'm1': 5,
        'core 5': 5,
        'm3': 6,
        'r7': 7,
        'ryzen 7': 7,
        'i7': 7,
        'ultra 7': 7,
        'm3 pro': 7,
        'core 7': 7,
        'ryzen 9': 9,
        'i9': 9,
        'ultra 9': 9,
        'm3 max': 9
    }

    # Menyusun daftar kata kunci untuk pencocokan
    keywords = cpu_mapping.keys()

    # Default value jika tidak ada kata kunci yang cocok
    temp_cpu = 3

    # Mencari kecocokan kata kunci dalam proc
    for keyword in keywords:
        if keyword in proc.lower():
            temp_cpu = cpu_mapping[keyword]
            break

    return temp_cpu

def tampil():
    try:
        # laptop = Laptop.query.all()
        laptops = Laptop.query.all()
        num_laptops = min(7, len(laptops))

        result.clear()
        nilai_price.clear()
        nilai_cpu.clear()
        nilai_ram.clear()
        nilai_storage.clear()

        for laptop in laptops:
        # for i in range(num_laptops):
        #     laptop = laptops[i]
            cpu = laptop.cpu
            proc = cpu.lower()
            separator = '{:,}'.format(laptop.price).replace(',','.')

            temp = val_cpu(proc)
            nilai_cpu.append(temp)

            result.append(
                {
                    'id': laptop.id,
                    'name':laptop.name,
                    'cpu': laptop.cpu,
                    'gpu': laptop.gpu,
                    'storage': laptop.storage,
                    'ram': laptop.ram,
                    'display': laptop.display,
                    'weight': laptop.weight,
                    'price': separator,
                    # 'temp_cpu': temp,
                }
            )

            nilai_price.append(laptop.price)
            # print(nilai_cpu)
            nilai_ram.append(laptop.ram)
            nilai_storage.append(laptop.storage)

            # temp = i.gpu
            # vga = temp.lower()
            # gpu = vga.replace(" ", "")
            # gpu_list.append(gpu)
            
            # if 'rtx40' in gpu or 'm3max' in gpu:
            #     nilai = 9
            # elif 'rtx30' in gpu:
            #     nilai = 8

            # elif 'm3pro' in gpu :
            #     nilai = 7
            # elif 'radeonrx' in gpu or 'm3' in gpu or 'arc' in gpu or 'rtx20' in gpu or 'rx' in gpu:
            #     nilai = 6

            # elif 'm2' in gpu or 'irisx' in gpu or 'gtx' in gpu :
            #     nilai = 5
            # elif 'm1' in gpu  :
            #     nilai = 4

            # elif 'radeonvega' in gpu :
            #     nilai = 2
            # elif 'integrated' in gpu or 'uhd' in gpu:
            #     nilai = 1
            # else:
            #     nilai = 3

            # nilai_gpu.append(nilai)
            # nilai_display.append(i.display)
            # nilai_name.append(i.name)
        
        # print(nilai_cpu)
        # jml_gpu = len(nilai_price)
        # print(f"banyak price {jml_gpu}")

        return jsonify(result)
    except Exception as e:
        print(e)
    
    # return None

def filter_laptop():
    try:
        data = request.json
        print(f'\n{data}')

        filters = data['filters'] # berisi ['Apple', 'Multimedia', '16']
        print(filters)

        laptop = Laptop.query.all()
        category = ''
        # filtered_laptops = []

        result.clear()
        nilai_price.clear()
        nilai_cpu.clear()
        nilai_ram.clear()
        nilai_storage.clear()
        
        def _filter(i):
            cpu_name = i.cpu.lower()
            temp = val_cpu(cpu_name)

            gpu_name = i.gpu.lower()
            if any(keyword in gpu_name for keyword in ['intel', 'iris', 'integrated']):
                category = 'Internet'
            elif any(keyword in gpu_name for keyword in ['nvidia', 'rtx', 'rx']):
                category = 'Gaming'
            else:
                category = 'Multimedia'

            cpu_filters = {
                'ryzen 3': 'AMD Ryzen 3',
                'r3': 'AMD Ryzen 3',
                'ryzen 5': 'AMD Ryzen 5',
                'r5': 'AMD Ryzen 5',

                'ryzen 7': 'AMD Ryzen 7',
                'r7': 'AMD Ryzen 7',
                'ryzen 9': 'AMD Ryzen 9',
                'r9': 'AMD Ryzen 9',
                
                'i3': 'Intel Core i3',
                'core 3': 'Intel Core i3',
                'i5': 'Intel Core i5',
                'ultra 5': 'Intel Core i5',
                
                'i7': 'Intel Core i7',
                'ultra 7': 'Intel Core i7',
                'i9': 'Intel Core i9',
                'ultra 9': 'Intel Core i9',
            }

            if (
                (filters[0] == "Semua" or filters[0] == i.brand) and
                (filters[1] == "Semua" or filters[1] == category) and
                # (filters[2] == "Semua" or int(filters[2]) == i.display) and
                
                (filters[2] == "Semua" or 
                 (filters[2] == '13 - 15' and 13.0 <= i.display < 16.0) or
                 (filters[2] == '16 - 18' and 16.0 <= i.display < 19.0)) and
                
                (filters[3] == "Semua" or 
                 (filters[3] == '1kg - 2kg' and 1.0 <= i.weight <= 2.0) or 
                 (filters[3] != '1kg - 2kg' and i.weight > 2.0)) and
                
                (filters[4] == "Semua" or any(key in cpu_name for key, value in cpu_filters.items() if filters[4] == value)) and
                (filters[5] == "Semua" or
                 (filters[5] == 'AMD' and 'amd' in gpu_name) or
                 (filters[5] == 'Intel' and ('intel' in gpu_name or 'integrated' in gpu_name)) or
                 (filters[5] == 'Nvidia' and 'nvidia' in gpu_name))
            ):
                nilai_price.append(i.price)
                # nilai_name.append(i.name)
                nilai_cpu.append(temp)
                nilai_ram.append(i.ram)
                nilai_storage.append(i.storage)
                
                separator = '{:,}'.format(i.price).replace(',','.')
                result.append({
                    'id': i.id,
                    'name': i.name,
                    'cpu': i.cpu,
                    'gpu': i.gpu,
                    'storage': i.storage,
                    'ram': i.ram,
                    'display': i.display,
                    'weight': i.weight,
                    'price': separator,
                })

        for i in laptop:
            _filter(i)

        print(len(nilai_price))
        print(len(nilai_cpu))
        print(len(nilai_ram))
        print(len(nilai_storage))

        response = {
            # "CR": j,
            "filtered_laptops": result,
        }
        # print(response)
        return jsonify(response)
    
    except Exception as e:
        print(e)