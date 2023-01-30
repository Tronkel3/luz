# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 20:58:20 2023

@author: javil
"""

import streamlit as st
import pandas as pd

st.title('Busca tu mejor oferta')

st.markdown("""
Encuentra el precio más barato para tus necesidades
""")

def load_data():
    df = pd.read_csv('precios.csv', encoding='utf-8', delimiter=';')
    return df
df = load_data()

def calcula_factura_todas(periodo_fact, energia_utilizada, potencia_contratada):
    empresas = df['Empresa'].tolist()
    data = df.to_numpy().tolist()
    empresas = []
    resul = {}
    for emp in data:
        empresas.append(emp[0])
        prcs_energia = emp[1:4]
        prcs_potencia = emp[4:6]

        ## ENERGÍA ##
        prc_energia_bruto = 0     

        # Datos
        energia_peaje_punta = 0.027787
        energia_peaje_llano = 0.019146 
        energia_peaje_valle = 0.000703
        energia_peajes = [energia_peaje_punta, energia_peaje_llano, energia_peaje_valle]
        prc_peajes_energia = 0

        energia_cargo_punta = 0.046622
        energia_cargo_plano = 0.009324
        energia_cargo_valle = 0.002331
        energia_cargos = [energia_cargo_punta, energia_cargo_plano, energia_cargo_valle]
        prc_cargos_energia = 0

        # Calcular facturación por energía utilizada
        for precio,consumo in zip(prcs_energia, energia_utilizada):
            prc_energia_bruto += (precio*consumo)

        for precio,consumo in zip(energia_peajes, energia_utilizada):
            prc_peajes_energia += (precio*consumo)

        for precio,consumo in zip(energia_cargos, energia_utilizada):
            prc_cargos_energia += (precio*consumo)

        precio_final_energia = prc_energia_bruto + prc_peajes_energia + prc_cargos_energia

        #################################

        ## POTENCIA ##
        prc_potencia_bruto = 0

        # Datos
        pot_peaje_punta = 22.988256
        pot_peaje_valle = 0.93889
        pot_cargo_punta = 3.175787
        pot_cargo_valle = 0.204242

        # Calcular facturación por potencia contratada
        for precio in prcs_potencia:
            prc_potencia_bruto += precio
        prc_potencia_bruto = (prc_potencia_bruto * potencia_contratada * periodo_fact) / 365    

        prc_potencia_peajes = ((pot_peaje_punta + pot_peaje_valle) * potencia_contratada * periodo_fact) / 365
        prc_potencia_cargos = ((pot_cargo_punta + pot_cargo_valle) * potencia_contratada * periodo_fact) / 365

        precio_final_potencia = prc_potencia_bruto + prc_potencia_peajes + prc_potencia_cargos

        #################################

        ## IMPUESTOS ##

        # Datos
        impuesto_electr = 0.005  
        iva = 0.05               
        alquiler_cont = 0.02663
        importe_iberico = 0.017785
        kW_consumidos = sum(energia_utilizada)

        # Calcular el precio de la factura con los impuestos
        prc_bruto = precio_final_energia + precio_final_potencia
        precio_factura = prc_bruto + (prc_bruto * impuesto_electr) + (prc_bruto * iva) + (periodo_fact * alquiler_cont) + (kW_consumidos * importe_iberico) 
        
        resul[emp[0]] = float(f'{precio_factura:.4f}')
    
    return resul

p = st.number_input('Potencia contratada')
ep = st.number_input('Energía utilizada punta')
el = st.number_input('Energía utilizada llano')
ev = st.number_input('Energía utilizada valle')

r = (calcula_factura_todas(30, [ep, el, ev], p))
df_r = pd.DataFrame()
df_r['Empresa'] = r.keys()
df_r['Precios'] = r.values()

minimo = list(r.keys())[0]
for em, pr in sorted(r.items()):
    if pr < r[minimo]:
        minimo = em

st.markdown(f'La empresa más barata es {minimo}: {r[minimo]}€')        
st.line_chart(df_r, x='Empresa', y='Precios')
st.bar_chart(df_r, x='Empresa', y='Precios')
        
