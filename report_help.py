# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd 
import streamlit as st
import math
import numpy as np
from biothings_client import get_client

#initialize
mv = get_client('variant')

#CSS to inject contained in a string
hide_table_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
    """

st.markdown(hide_table_index, unsafe_allow_html=True)


transcript_list = pd.read_csv(r'C:\Users\13060119\transcript_list.txt',sep='\t')

test = pd.read_csv(r'C:\Users\13060119\Desktop\transcripts.txt',sep='\t')
test["CDS length"] = test["CDS length"].astype('Int64')

transcript_list["Length of CDS"] = transcript_list["Length of CDS"].astype('Int64')

tab1, tab2, tab3, tab4 = st.tabs(["Befund", "A posteriori", "HGMD batch","Listenvergleich"])

with tab1:
    st.title('Befundhilfe')
    
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])
    with col1:
        name = st.text_input('Genname', placeholder= "e.g. CFTR")
        #name = st.selectbox('Genname',gene_list["Genname"])
        
    # gene = mv.query(name)
    # if type(gene["hits"][0]["snpeff"]["ann"]) is dict:
    #     df = pd.DataFrame({'Genname': gene["hits"][0]["snpeff"]["ann"]["genename"],
    #                   'Transkript': gene["hits"][0]["snpeff"]["ann"]["feature_id"],
    #                   'CDS Länge': gene["hits"][0]["snpeff"]["ann"]["cds"]["length"]}, index = [0])
    # else:
    #     df = pd.DataFrame({'Genname': gene["hits"][0]["snpeff"]["ann"][0]["genename"],
    #                   'Transkript': gene["hits"][0]["snpeff"]["ann"][0]["feature_id"],
    #                   'CDS Länge': gene["hits"][0]["snpeff"]["ann"][0]["cds"]["length"]}, index = [0])
    # st.table(df)


    st.write("Transkript")
    transcr = transcript_list[transcript_list["Approved symbol"] == name.upper()]
    # trans2 = test[test['Gene symbol'] == name.upper()]
    st.table(transcr) 
    
    gene_250 = 0
    if transcr["Length of CDS"].any():
        gene_len = transcr["Length of CDS"]
        gene_250 = math.floor(gene_len/250)
    
    with col2:
        gene_mode = st.radio('Befundart',('Einzelgen','Ausschluss'))
    
    with col3:
        inheritance = st.radio('Vererbung', ('AR','AD','XLR', 'XLD'))
    
    with col4:
        allele  = st.radio('Zygotie',('heterozygot','homozygot'))
    
    with col5:
        st.write('VUS')
        VUS = st.checkbox('VUS')
    n_variants = st.slider('Anzahl Varianten',0,2,1)
    
    if name.lower() == 'cftr' and n_variants ==2:
        all_panel = st.checkbox('Alle Varianten im Panel')
    
    if gene_mode == 'Einzelgen' and (gene_250 < 6):
        n_dm = st.number_input('Anzahl DM Varianten:', 0)
    # if gene_list[gene_list["Genname"] == name.upper()]:
    
    
    desc = 'unauffällig'
    hgvs = ''
    
    if n_variants > 0:
        if inheritance == 'AD':
            desc = 'Anlageträger bzw. erkrankt'
            if allele == 'heterozygot':
                hgvs = 'c.Variante (het.)'
            else:
                hgvs = 'c.Variante (hom.)'
        elif inheritance == 'AR':
            if allele == 'heterozygot':
                if n_variants == 1:
                    if gene_mode == 'Einzelgen':
                        hgvs = 'c.[Variante];[=]'
                    else:
                        hgvs = 'c.[Variante];[Position=]'
                    desc = 'Überträgerstatus'
                elif n_variants == 2:
                    desc = 'auffällig'
                    hgvs = 'c.Variante1(;)Variante2  \n falls Phänotyp sehr gut passt:  \n c.[Variante1];[Variante2]'
            else:
                desc = 'auffällig'
                hgvs = 'c.[Variante];[Variante]'
        elif inheritance == 'XLR':
            if n_variants == 2:
                desc = 'erkrankt'
                if allele == 'heterozygot':
                    hgvs = 'weiblich:  \n c.[Variante1];[Variante2]'
                else:
                    hgvs = 'weiblich:  \n c.[Variante];[Variante]'
            else:
                desc = 'weiblich: Konduktorinnenstatus  \n männlich: erkrankt'
                hgvs = 'weiblich: c.[Variante];[=]  \n männlich: c.[Variante];[0]'
        elif inheritance == 'XLD':
            desc = 'Anlageträger bzw. erkrankt'
            hgvs = 'c.Variante'
        if VUS:
            if inheritance == 'AD' or inheritance == 'XLD':
                desc = 'Trägerschaft'
                if allele == 'heterozygot':                    
                    hgvs = 'c.Variante (het.)'
                else:
                    hgvs = 'c.Variante (hom.)'
            elif inheritance == 'AR' or inheritance == 'XLR':
                desc = 'Trägerschaft'
                if n_variants == 2:
                    if allele == 'heterozygot':
                        hgvs = 'c.Variante1(;)Variante2'
                    else:
                        hgvs = 'c.[Variante];[Variante]'
                elif allele == 'homozygot':
                    hgvs = 'c.[Variante];[Variante]'
                else:
                    hgvs = 'c.[Variante];[?]'
         
    
         
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Anhänge:")
        st.write('NGS anhängen')
        st.write('ggf. MLPA bzw. qPCR anhängen')
        st.write('ggf. Sanger anhängen')
        if name.lower() == 'cftr':
            st.write('Screenshot 7T Allel')
            st.write('Screenshot cftr2.org')
        if name.lower() == 'pah':
            st.write('Screenshot BioPKU')
        if gene_mode == 'Ausschluss' and (n_variants == 0):
            st.write('MutA anhängen')
        
    with c2:
        st.subheader("Befund:")
        st.write(desc)
        st.write(hgvs)
        if name.lower() == 'cftr' and (n_variants < 2 or (n_variants > 1 and not all_panel)):
            st.write("2. Befund")
     
    with c3:
        st.subheader("Abrechnung:")
        if name.lower() == 'cftr':
            st.write("11351: 1x")
            if (n_variants < 2 or (n_variants == 2 and not all_panel)):
                st.write("11352: 1x")
                
        elif gene_mode == 'Einzelgen':
            if gene_250 < 6 and (n_dm/3 >= gene_250):
                if n_dm > 14:
                    st.write("11511: x15")
                else:
                    st.write("11511: x" + str(n_dm))
            else:
                st.write("11513: x" + str(gene_250))
        else:
            st.write("11518: x1")
        
with tab4:
    
    # use_tabs = st.checkbox('Nutze Leerzeichen als Trennzeichen')
    tc1, tc2 = st.columns(2)
    # get gene lists
   
    genes1_txt = tc1.text_area("Genliste 1")
    genes2_txt = tc2.text_area("Genliste 2")
    
    genes1 = [k.strip().upper() for k in genes1_txt.replace('\n',' ').replace(',',' ').split()]           
    genes2 = [k.strip().upper() for k in genes2_txt.replace('\n',' ').replace(',',' ').split()]  

    seen1 = set()
    genes1_unique = [x for x in genes1 if x.upper() not in seen1 and not seen1.add(x.upper())]
    seen2 = set()
    genes2_unique = [x for x in genes2 if x.upper() not in seen2 and not seen2.add(x.upper())]
   
    # print length of lists
    if genes1 != [""]:
        tc1.write("Länge der 1. Genliste: " + str(len(genes1_unique)))
        

    # check if genes in lists are unique
    if len(genes1) != len(genes1_unique):
        dup_genes1 = list(set([x for x in genes1 if genes1.count(x.upper()) > 1]))
        dup_genes1.sort()
        tc1.write("Folgende Gene kommen mehrfach vor: %s" % ', '.join(map(str, dup_genes1)))

    
    diff1 = set(genes1_unique) - set(genes2_unique)
    diff2 = set(genes2_unique) - set(genes1_unique)
    # if genes2 != [""]:
    
    # if np.logical_and(use_tabs, len(genes2_unique) > 0) or np.logical_and(not use_tabs, genes2 != [""]):
    # print(genes2)
    if genes2 != []:
        tc2.write("Länge der 2. Genliste: " + str(len(genes2_unique)))
        
        # check if genes in lists are unique
        if len(genes2) != len(genes2_unique):
            dup_genes2 = list(set([x for x in genes2 if genes2.count(x.upper()) > 1]))
            dup_genes2.sort()
            tc2.write("Folgende Gene kommen mehrfach vor: %s" % ', '.join(map(str, dup_genes2)))

        if len(diff1) > 0:
            tc1.write("Folgende Gene nur in 1. Liste: %s" % ', '.join(map(str, list(diff1))))
        if len(diff2) > 0:
            tc2.write("Folgende Gene nur in 2. Liste: %s" % ', '.join(map(str, list(diff2))))
        
        if len(diff1) == 0 and (len(diff2) == 0):
            st.write("Die beiden Genlisten sind identisch.")

        
    
with tab2: 
    st.write("A posteriori Risiko")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        prevalence = st.number_input('Prävalenz 1 zu',1, value = 10000, step = 1000)
    with p2:
        # risk = st.number_input('Gesicherter Überträger',0.0,1.0, value = 0.5, step = 0.5)
        carrier  = st.radio('Überträger',('heterozygot','homozygot'))
    with p3:
        detection_rate = st.number_input('Detektionsrate',0.0,1.0, value = 0.95)
        
    if carrier == 'heterozygot':
        risk = .5
    else:
        risk = 1
        
    q_2 = 1/prevalence
    q = np.sqrt(q_2)
    p = 1-q
    pq2 = 2*p*q
    
    detection = 1-detection_rate
    posteriori = .5*risk*detection*pq2
    
    dat = {'Allelfrequenz': ['q²','p','q','2pq', 'A Posteriori'],'percentage':[q_2, p, q, pq2, posteriori],'Anteil (1:x)':[1/q_2, 1/p, 1/q, 1/pq2, 1/posteriori]}
    df = pd.DataFrame(dat)

    # st.table(df)
    st.table(df.style.format({"percentage": "{:.6f}", "Anteil (1:x)":"{:.0f}"}))
    
with tab3:
    
    tab4_c1, tab4_c2 = st.columns(2)
    
    with tab4_c1:
        genes_txt = st.text_area("Genliste")
    
    # genes_out = genes_txt.replace('  \n',',').split(',').strip()
    genes_out = [k.strip().upper() for k in genes_txt.replace('\n',',').split(',')]
    genes_out_u = list(np.unique(genes_out))
    if "" in genes_out_u:
        genes_out_u.remove("")

    with tab4_c2:
        st.text_area("HGMD sytle Liste", '\n'.join(genes_out_u))
    # hgmd_df = pd.DataFrame(genes_out_u)
    # style = hgmd_df.style.hide_index()
    # style.hide_columns()
    # C:\Users\13060119\.spyder-py3\temp.py:280: FutureWarning: this method is deprecated in favour of `Styler.hide(axis='columns')`
    # st.table(hgmd_df)
        

#%% Variant stuff


# with tab2:

#     #create container to contain everything
#     c = st.container()
    
    
#     c.write('\nVariant stuff')
#     var = mv.getvariant(c.text_input('variante'))
    
    
#     if var:
#         #create 3 columsn for output
#         var_c1, var_c2, var_c3 = c.columns(3)
        
        
#         #column 1
#         #CDS length and transcript
#         if "snpeff" in var:
#             if type(var["snpeff"]["ann"]) is dict:
#                 var_c1.write("CDS-Länge: " + str(var["snpeff"]["ann"]["cds"]["length"]))
#             else:
#                 var_c1.write("CDS-Länge: " + str(var["snpeff"]["ann"][-1]["cds"]["length"]))
        
#         if "civic" in var:
#             var_c1.write("Transkript: " + var["civic"]["hgvs_expressions"][0].split(":")[0])
        
#         #column 2
#         #gnomad MAF and het/hom    
#         var_c2.subheader("gnomAD:")
#         if "gnomad_exome" in var:
#             var_c2.write("MAF: " + str(var["gnomad_exome"]["af"]["af"]))
#             var_c2.write("heterozygot: x" + str(var["gnomad_exome"]["ac"]["ac"]))
#             var_c2.write("homozgyot: x" + str(var["gnomad_exome"]["hom"]["hom"]))
                         
                 
#         #column 3
#         #clinvar
#         var_c3.subheader("ClinVar:")
#         if "clinvar" in var:
#             clinvar_list = []
#             if type(var["clinvar"]["rcv"]) is dict:
#                 clinvar_list.append(var["clinvar"]["rcv"]["clinical_significance"])
#             else:
#                 for k in var["clinvar"]["rcv"]:
#                     clinvar_list.append(k["clinical_significance"])
        
        
#             var_c3.write("ID: " + str(var["clinvar"]["variant_id"]))
            
#             for classification in ['Pathogenic', 'Likely pathogenic', 'Uncertain significane', 'Likely benign', 'Benign']:
#                 clin_count = clinvar_list.count(classification)
#                 if clin_count:
#                     var_c3.write(classification + ": x" + str(clin_count))



    