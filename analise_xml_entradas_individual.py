import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import xml.etree.ElementTree as ET
import csv
import os
import pandas as pd

import base64
from io import BytesIO
from PIL import Image, ImageTk

# Variáveis para armazenar os caminhos
destino = ''
origem =''
def selecionar_caminho_xml():
    origem = filedialog.askdirectory(title="Selecione o diretório dos arquivos XML")
    entrada_btn_arquivo.delete(0, tk.END)
    entrada_btn_arquivo.insert(0, origem)

def selecionar_caminho_relatorio():
    destino = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Nomeie o arquivo para salvar o relatório")
    entrada_btn_arquivo2.delete(0, tk.END)
    entrada_btn_arquivo2.insert(0, destino)

def executar():
    produtos = {}



    def retornar_valor_total_itens(caminho):
        valor_total_itens=0	

        # Defina o namespace
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Carregue o arquivo XML
        tree = ET.parse(caminho)

        # Obtenha o elemento raiz
        root = tree.getroot()

        notafiscal= root.find('.//nfe:ide', namespace)

        # Exemplo para extrair informações do produto:
        det = root.findall('.//nfe:det', namespace)
    
        for items_det in det:
            #valor_total_itens = 
            valor_em_texto=float(items_det.find('./nfe:prod/nfe:vProd', namespace).text)
            valorTotal=float(valor_em_texto)
            valor_total_itens = valorTotal+valor_total_itens
            
        return valor_total_itens

    def inserir_produto(nome, codigo, data, undMedida, vrUnitario,qtdItem,fornecedor,cnpj,custoTotalItem,NFE,CHAVE):
        if nome not in produtos:
            produtos[nome] = []
        produtos[nome].append({ "nome":nome,
                                "codigo": codigo,
                                "data": data,
                                "undMedida":undMedida,
                                "valorUnitario":vrUnitario,
                                "quantidade":qtdItem,
                                "fornecedor":fornecedor,
                                "cnpj":cnpj,
                                "custo": custoTotalItem,
                                "NFE":NFE,
                                "CHAVE":CHAVE
                                })


    def leituraXML(caminho):
        #total somado dos valores dos itens
        somaTotalItensNota=0
        somaTotalItensNota=retornar_valor_total_itens(caminho)
        
        # Defina o namespace
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Carregue o arquivo XML
        tree = ET.parse(caminho)

        # Obtenha o elemento raiz
        root = tree.getroot()

        notafiscal= root.find('.//nfe:ide', namespace)

        # Use o namespace ao buscar elementos
        # Exemplo para extrair informações do emitente e do destinatário:
        emitente = root.find('.//nfe:emit', namespace)

        totalLiquidoNota= root.find('.//nfe:cobr/nfe:fat', namespace)

        valorLiquidoNotaFiscal="" #evita erros na gravação do excel

        ICMSTot = root.find('.//nfe:ICMSTot', namespace)

        try:
            if totalLiquidoNota is not None:
                valorLiquidoNotaFiscal = totalLiquidoNota.find('nfe:vLiq', namespace).text

            else:
                if (valorLiquidoNotaFiscal==""):
                    totalLiquidoNota= root.find('.//nfe:detPag', namespace)
                    valorLiquidoNotaFiscal = totalLiquidoNota.find('./nfe:vPag', namespace).text
                if(valorLiquidoNotaFiscal=="0.00" or valorLiquidoNotaFiscal=="0"):
                    valorLiquidoNotaFiscal=ICMSTot.find('./nfe:vNF', namespace).text #evita erros na gravação
                    #print("AAqui!-> " + valorLiquidoNotaFiscal)
        except:

            try:
                totalLiquidoNota= root.find('.//nfe:pag', namespace)
                valorLiquidoNotaFiscal = totalLiquidoNota.find('nfe:vPag', namespace).text

            except:
                valorLiquidoNotaFiscal=ICMSTot.find('./nfe:vNF', namespace).text #evita erros na gravação
                pass



    #   ICMSTot = root.find('.//nfe:ICMSTot', namespace)


        vBC= 0 #evita erros na gravação
        vICMS= 0  #evita erros na gravação
        vICMSDeson= 0 #evita erros na gravação
        vFCPUFDest= 0  #evita erros na gravação
        vICMSUFDest= 0  #evita erros na gravação
        vICMSUFRemet= 0 #evita erros na gravação
        vFCP= 0  #evita erros na gravação
        vBCST= 0#evita erros na gravação
        vST= 0#evita erros na gravação
        vFCPST= 0#evita erros na gravação
        vFCPSTRet= 0#evita erros na gravação
        vProd= 0#evita erros na gravação
        vFrete= 0#evita erros na gravação
        vSeg= 0#evita erros na gravação
        vDesc= 0#evita erros na gravação
        vII= 0#evita erros na gravação
        vIPI= 0#evita erros na gravação
        vIPIDevol= 0#evita erros na gravação
        vPIS= 0#evita erros na gravação
        vCOFINS=0#evita erros na gravação
        vOutro   = 0#evita erros na gravação

        try:
            if ICMSTot is not None:
                vBC= ICMSTot.find('./nfe:vBC', namespace).text #evita erros na gravação
                #print("ok1")
                vICMS= ICMSTot.find('./nfe:vICMS', namespace).text  #evita erros na gravação
                #print("ok2")
                vICMSDeson= ICMSTot.find('./nfe:vICMSDeson', namespace).text #evita erros na gravação
                #print("ok3")
                vFCPUFDest=0 # ICMSTot.find('./nfe:vFCPUFDest', namespace).text  #evita erros na gravação
                #print("ok4")
                vICMSUFDest= 0 #ICMSTot.find('./nfe:vICMSUFDest', namespace).text  #evita erros na gravação
                #print("ok5")
                vICMSUFRemet= 0#ICMSTot.find('./nfe:vICMSUFRemet', namespace).text  #evita erros na gravação
                #print("ok6")
                vFCP= ICMSTot.find('./nfe:vFCP', namespace).text  #evita erros na gravação
                #print("ok7")
                vBCST=  0# ICMSTot.find('./nfe:vBCST', namespace).text #evita erros na gravação
                #print("ok8")
                vST= ICMSTot.find('./nfe:vST', namespace).text #evita erros na gravação
                #print("ok9")
                            
                vFCPST= ICMSTot.find('./nfe:vFCPST', namespace).text #evita erros na gravação
                #print("ok10")
                vFCPSTRet= ICMSTot.find('./nfe:vFCPSTRet', namespace).text #evita erros na gravação
                #print("ok11")
                vProdTOTAL= ICMSTot.find('./nfe:vProd', namespace).text #evita erros na gravação
                #print("ok12")
                vFrete= ICMSTot.find('./nfe:vFrete', namespace).text  #evita erros na gravação
                #print("ok13")
                vSeg= ICMSTot.find('./nfe:vSeg', namespace).text  #evita erros na gravação
                #print("ok13")
                vDesc= ICMSTot.find('./nfe:vDesc', namespace).text #evita erros na gravação
                #print("ok15")
                vII= 0# ICMSTot.find('./nfe:vII', namespace).text #evita erros na gravação
                #print("ok16")
                vIPI= ICMSTot.find('./nfe:vIPI', namespace).text #evita erros na gravação
                #print("ok17")
                vIPIDevol= 0# ICMSTot.find('./nfe:vIPIDevol', namespace).text #evita erros na gravação
                #print("ok18")
                vPIS= ICMSTot.find('./nfe:vPIS', namespace).text #evita erros na gravação
                #print("ok19")
                vCOFINS= ICMSTot.find('./nfe:vCOFINS', namespace).text #evita erros na gravação
                #print("ok20")
                vOutro   = ICMSTot.find('./nfe:vOutro', namespace).text #evita erros na gravação
                #print("ok21")
        except:
            pass

        # Encontrar o elemento ICMS60

        icms60 = root.find('.//nfe:ICMS60', namespace)
        # Se o elemento ICMS60 foi encontrado, extrair os valores desejados

        vBCSTRet = 0           #evita erros na gravação do excel
        pST = 0                 #evita erros na gravação do excel
        vICMSSubstituto = 0     #evita erros na gravação do excel
        vICMSSTRet= 0               #evita erros na gravação do excel
        pRedBCEfet= 0           #evita erros na gravação do excel
        vBCEfet= 0              #evita erros na gravação do excel
        pICMSEfet= 0          #evita erros na gravação do excel
        vICMSEfet = 0           #evita erros na gravação do excel
        cst60=0


        icms40 = root.find('.//nfe:ICMS40', namespace)
        cst40=""

        chave_nfe=""    #evita erros na gravação do excel

        chave_nota_fiscal=root.find('.//nfe:protNFe/nfe:infProt', namespace)

        try:
            if chave_nota_fiscal is not None:
                chave_nfe = chave_nota_fiscal.find('nfe:chNFe', namespace).text
        except:
            pass

        num_nota_fiscal=""    #evita erros na gravação do excel
        data_entrada_saida=""

        try:
            if notafiscal is not None:
                num_nota_fiscal = notafiscal.find('nfe:nNF', namespace).text
                data_entrada_saida=(notafiscal.find('nfe:dhEmi', namespace).text)[:10]
        except:
            try:
                data_entrada_saida=(notafiscal.find('nfe:dhSaiEnt', namespace).text)[:10]

            except:

                pass

        nome_emitente=""    #evita erros na gravação do excel
        cnpj_emitente=""    #evita erros na gravação do excel

        try:
            if emitente is not None:
                nome_emitente = emitente.find('nfe:xNome', namespace).text
                try:
                    cnpj_emitente ="'"+ emitente.find('nfe:CNPJ', namespace).text
                except:
                    cnpj_emitente ="'"+ emitente.find('nfe:CPF', namespace).text


                #print(f'Nome do Emitente: {nome_emitente}')
        except:
            pass

        destinatario = root.find('.//nfe:dest', namespace)

        nome_destinatario=""    #evita erros na gravação do excel


        # Exemplo para extrair informações do produto:
        det = root.findall('.//nfe:det', namespace)
        codigo_produto=""
        vDescItem= 0#evita erros na gravação
        NCM =""    #evita erros na gravação do excel
        CFOP=""    #evita erros na gravação do excel
        unidadeMedida=""    #evita erros na gravação do excel
        qtd=0    #evita erros na gravação do excel
        valorUnitario =0    #evita erros na gravação do excel
        valor =0    #evita erros na gravação do excel
        ICMS00=""    #evita erros na gravação do excel
        ICMS10=""    #evita erros na gravação do excel
        ICMS20=""    #evita erros na gravação do excel
        ICMS30=""    #evita erros na gravação do excel
        ICMS40=""    #evita erros na gravação do excel
        ICMS41=""    #evita erros na gravação do excel
        ICMS50=""    #evita erros na gravação do excel
        ICMS51=""    #evita erros na gravação do excel
        ICMS70=""    #evita erros na gravação do excel
        ICMS90=""    #evita erros na gravação do excel
        ICMSST=""


        vST_arredondado = float(vST)          #NECESSARIO MANTER ESSE ESCOPO PARA NAO PERDER O TOTAL VIPI_VST
        vIPI_arredondado = float(vIPI)#NECESSARIO MANTER ESSE ESCOPO PARA NAO PERDER O TOTAL VIPI_VST
        VIPIVST= vST_arredondado+vIPI_arredondado   #NECESSARIO MANTER ESSE ESCOPO PARA NAO PERDER O TOTAL VIPI_VST
        vDescItemProporcional=0             #NECESSARIO MANTER ESSE ESCOPO PARA NAO PERDER O TOTAL VIPI_VST

        for items_det in det:			#OBS: frete geralmente só aparece 1 vez...ao percorrer os itens a informacao pode ser zerada (frete)
            #print (det)

            NCM = items_det.find('./nfe:prod/nfe:NCM', namespace)
            try:
                vDescItem=items_det.find  ('./nfe:prod/nfe:vDesc', namespace).text
            except:
                vDescItem=0
            descricao = items_det.find('./nfe:prod/nfe:xProd', namespace).text.replace('\n', '').replace(';', '')
            CFOP= items_det.find('./nfe:prod/nfe:CFOP', namespace).text
            unidadeMedida= items_det.find('./nfe:prod/nfe:uCom', namespace).text
            qtd= items_det.find('./nfe:prod/nfe:qCom', namespace).text
            valorUnitario = items_det.find('./nfe:prod/nfe:vUnCom',namespace).text
            valor = items_det.find('./nfe:prod/nfe:vProd', namespace).text
            codigo_produto=items_det.find('./nfe:prod/nfe:cProd', namespace).text

            paths = [
            './nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS40/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS70/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS90/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMSST/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS20/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS10/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS30/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN101/nfe:CSOSN',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN102/nfe:CSOSN',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN201/nfe:CSOSN',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN500/nfe:CSOSN',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN900/nfe:CSOSN',
            './nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:CST',
            './nfe:imposto/nfe:ICMS/nfe:ICMS61/nfe:CST'
    ]

            cst60 = None
            for path in paths:
                try:
                    cst60 = items_det.find(path, namespace).text
                    break
                except:
                    continue

            if cst60 is None:
                # Handle the case where none of the paths returned a result
                print("Não localizado o CST/CSOSN corrija!!!.")



            #vICMSDeson (vICMSDeson) adicionado em 18-10-2024
            paths = [
            './nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS40/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS70/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS90/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSST/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS20/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS10/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS30/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN101/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN102/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN201/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN500/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMSSN900/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:vICMSDeson',
            './nfe:imposto/nfe:ICMS/nfe:ICMS61/nfe:vICMSDeson'
    ]
            vICMSDeson = ""
            for path in paths:
                try:
                    vICMSDeson = items_det.find(path, namespace).text
                    break
                except:
                    continue

                






            if NCM is not None:
                pass

            try:

                valorUnd=float(valorUnitario)
                valorUnd=str(valorUnd).replace('.',',')
                qtdItens=float(qtd)
                qtdItens=str(qtdItens).replace('.',',')
                vrTotalItens=float(valor)
                
            

                vrLiquidoNotaFiscal=float(valorLiquidoNotaFiscal)
                vrLiquidoNotaFiscal=str(vrLiquidoNotaFiscal).replace('.',',')

                rateioIcmsPorItem=(vST_arredondado/float(vProdTOTAL)) * float(valor)    #rateio
                ipiRateadoItem=(vIPI_arredondado/float(vProdTOTAL)) * float(valor)      #rateio


                rateioIcmsPorItem=float(rateioIcmsPorItem)
                rateioIcmsPorItem=str(rateioIcmsPorItem).replace('.',',')

                ipiRateadoItem=float(ipiRateadoItem)
                ipiRateadoItem=str(ipiRateadoItem).replace('.',',')

                vrTotalItens=str(vrTotalItens).replace('.',',')

                if(float(vFCPST)>0):		#fcop (vFCPST) adicionado em 18-10-2024
                    vFCPST=float(vFCPST)
                    #vFCPST=str(vFCPST).replace('.',',')
                else:
                    vFCPST=0	
                try:			
                    if(float(vICMSDeson)>0):		#vICMSDeson (vICMSDeson) adicionado em 18-10-2024
                        vICMSDeson=float(vICMSDeson)
                    #vFCPST=str(vFCPST).replace('.',',')
                    else:
                        vICMSDeson=0
                except:
                    vICMSDeson=0
                    pass
                    
                    
                
                if(float(vDesc)>0):
                    descontoRateaItem= (float(vDesc)/somaTotalItensNota)* float(valor)
                    descontoRateaItem=descontoRateaItem
                    descontoRateaItem="-" + str(descontoRateaItem)
                    descontoRateaItem=str(descontoRateaItem).replace('.',',')
                    
                    #descontoRateaItem= (float(vDesc)/float(vProdTOTAL))* float(valor)
                    #descontoRateaItem=descontoRateaItem
                    #descontoRateaItem="-" + str(descontoRateaItem)
                    #descontoRateaItem=str(descontoRateaItem).replace('.',',')
                    

                else:
                    descontoRateaItem=0

                if(float(vFrete)>0):
                    freteRateado= (float(vFrete)/somaTotalItensNota)* float(valor)
                    freteRateado=freteRateado
                    freteRateado=str(freteRateado).replace('.',',')
                    
                    #freteRateado= (float(vFrete)/float(vProdTOTAL))* float(valor)
                    #freteRateado=freteRateado
                    #freteRateado=str(freteRateado).replace('.',',')				
                
                else:
                    freteRateado=0
                    
                



                if(float(vOutro)>0):
                    outrasDespesas= (float(vOutro)/float(vProdTOTAL))* float(valor)
                    outrasDespesas=outrasDespesas
                    outrasDespesas=str(outrasDespesas).replace('.',',')

                else:
                    outrasDespesas=0



                if(float(vSeg)>0):
                    seguroRateado= (float(vSeg)/float(vProdTOTAL))* float(valor)
                    seguroRateado=seguroRateado
                    seguroRateado=str(seguroRateado).replace('.',',')

                else:
                    seguroRateado=0

                #totalização custo final
                custoTotaldoItem= vFCPST - vICMSDeson+  float(valor)+ ((float(vFrete)/float(vProdTOTAL))* float(valor) ) + ((vIPI_arredondado/float(vProdTOTAL)) * float(valor) ) + ((vST_arredondado/float(vProdTOTAL)) * float(valor)) - ((float(vDesc)/float(vProdTOTAL))* float(valor)) +(float(vOutro)/float(vProdTOTAL))* float(valor)
                
                if(float(vFCPST)>0):		#fcop (vFCPST) adicionado em 18-10-2024
                    vFCPST=float(vFCPST)
                    vFCPST=str(vFCPST).replace('.',',') #para gravar corretamente no excel (valor somável)
                else:
                    vFCPST=0
                    
                if(float(vICMSDeson)>0):		#vICMSDeson (vICMSDeson) adicionado em 18-10-2024
                    vICMSDeson=float(vICMSDeson)
                    vICMSDeson="-"+str(vICMSDeson).replace('.',',')
                else:
                    vICMSDeson=0				
                    
                
                float_custoTotaldoItem=custoTotaldoItem
                custoTotaldoItem=custoTotaldoItem
                custoTotaldoItem=str(custoTotaldoItem).replace('.',',')


                aliquota=calcular_porcentagem(float(cst60))
                aliquota= float(aliquota)

                imposto = aliquota*float_custoTotaldoItem

                imposto=str(imposto).replace('.',',')

                writer.writerow([nome_emitente,
                                cnpj_emitente,
                                codigo_produto,
                                descricao,
                                valorUnd,  #valorUnitario
                                qtdItens, #quantidade
                                unidadeMedida,
                                vrTotalItens, #valor total dos itens
                                rateioIcmsPorItem,    #icms substituição rateado
                                vFCPST,
                                vICMSDeson,							
                                ipiRateadoItem,        #ipi individual
                                descontoRateaItem,  #desconto item
                                seguroRateado,    #valor seguro
                                freteRateado,     #valor freteF                            custoTotaldoItem, #custo total do item
                                outrasDespesas,
                                custoTotaldoItem,
                                cst60,
                                CFOP,
                                NCM.text,
                                num_nota_fiscal,
                                aliquota,
                                imposto,
                                vrLiquidoNotaFiscal, #valor liquido da nota fiscal
                                data_entrada_saida,
                                "'"+ chave_nfe,
                                vBCSTRet,pST,vICMSSubstituto,vICMSSTRet,pRedBCEfet,vBCEfet,pICMSEfet,vICMSEfet])

                print(f"Nota fiscal chave {chave_nfe} processada e ok!")


                cst40=""
                vBCSTRet = 0           #evita erros na gravação do excel
                pST = ""                 #evita erros na gravação do excel
                vICMSSubstituto = 0     #evita erros na gravação do excel
                vICMSSTRet= 0               #evita erros na gravação do excel
                pRedBCEfet= ""           #evita erros na gravação do excel
                vBCEfet= 0              #evita erros na gravação do excel
                pICMSEfet= ""            #evita erros na gravação do excel
                vICMSEfet = ""           #evita erros na gravação do excel
                cst60=""
                vBC= 0 #evita erros na gravação
                vICMS= 0  #evita erros na gravação
                vICMSDeson= 0 #evita erros na gravação
                vFCPUFDest= 0  #evita erros na gravação
                vICMSUFDest= 0  #evita erros na gravação
                vICMSUFRemet= 0 #evita erros na gravação
                vFCP= 0  #evita erros na gravação
                vBCST= 0#evita erros na gravação
                vST= 0#evita erros na gravação
                vFCPST= 0#evita erros na gravação
                vFCPSTRet= 0#evita erros na gravação
                vProd= 0#evita erros na gravação
                #vFrete= 0#evita erros na gravação			comentado em 18/10/2024
                #vSeg= 0#evita erros na gravação
                #vDesc= 0#evita erros na gravação
                vDescItem= 0#evita erros na gravação
                vII= 0#evita erros na gravação
                vIPI= 0#evita erros na gravação
                vIPIDevol= 0#evita erros na gravação
                vPIS= 0#evita erros na gravação
                vCOFINS= 0#evita erros na gravação
                #vOutro   = 0#evita erros na gravação
                ICMS00=""    #evita erros na gravação do excel
                ICMS10=""    #evita erros na gravação do excel
                ICMS20=""    #evita erros na gravação do excel
                ICMS30=""    #evita erros na gravação do excel
                ICMS40=""    #evita erros na gravação do excel
                ICMS41=""    #evita erros na gravação do excel
                ICMS50=""    #evita erros na gravação do excel
                ICMS51=""    #evita erros na gravação do excel
                ICMS70=""    #evita erros na gravação do excel
                ICMS90=""    #evita erros na gravação do excel
                ICMSST=""

                inserir_produto(descricao,codigo_produto, data_entrada_saida,unidadeMedida,valorUnd, qtdItens,nome_emitente,cnpj_emitente, custoTotaldoItem,num_nota_fiscal,chave_nfe)


            except Exception as e:  # Captura qualquer exceção
                print(f"Ocorreu um erro!")  # Exibe a mensagem da exceção
                if("float division by zero" in e):
                    print('A nota fiscal {} possui valor liquido igual a 0. Verifique!')
                else:

                    print("Erro na leitura da NFE: " + chave_nfe)
                    print("Descrição do erro: {e}")
                    print("pressione Enter para continuar...")
                    y=input()



    def calcular_porcentagem(valor):
        if round(valor,0) == 0:
            return 0.0
        elif round(valor,0) == 20:
            return 0.014
        elif 101 <= round(valor,0) <= 103:
            return 0.066
        else:
            return 0



    def extensao_arquivo(caminho):
        return os.path.splitext(caminho)[1]


    def ler_todos_arquivos_xml(diretorio):
        # Percorra todos os arquivos no diretório
        for raiz, subdiretorios, arquivos in os.walk(diretorio):
            for nome_arquivo in arquivos:
                caminho_completo = os.path.join(raiz, nome_arquivo)
                caminho_atualizado = caminho_completo.replace('\\', '\\\\')
                if ('.XML' in extensao_arquivo(caminho_completo).upper()):
                    try:

                        leituraXML(caminho_completo)
                    except:
                        pass

    def sanitize_filename(filename):
        # Lista de caracteres inválidos
        invalid_chars = '<>:"/\\|?*'

        # Elimina cada caractere inválido da string
        for char in invalid_chars:
            filename = filename.replace(char, '')

        # Remove caracteres ASCII de controle
        filename = ''.join(ch for ch in filename if 31 < ord(ch) < 127 or ch in ('\t', '\n', '\r'))

        # Evita nomes reservados no Windows
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        if filename.upper() in reserved_names:
            filename = '_' + filename

        # Evita espaços no início e no final do nome do arquivo
        filename = filename.strip()

        return filename

    def graficoCustoProduto(produto):

        import pandas as pd
        import matplotlib.pyplot as plt

        try:
            # Pegue as ocorrências do produto 'UVA VERDE'
            ocorrencias_uva_verde = produtos.get(produto, [])

            # Converta as ocorrências em um DataFrame
            df = pd.DataFrame(ocorrencias_uva_verde)




            # Ordene o DataFrame pela data para uma visualização sequencial
            df['data'] = pd.to_datetime(df['data'])
            df = df.sort_values(by='data')




            # Plote a variação do custo
            plt.figure(figsize=(10, 6))
            plt.plot(df['data'], df['valorUnitario'], marker='o', linestyle='-')

            # Defina os limites do eixo Y usando o mínimo e o máximo de valorUnitario
            plt.ylim(df['valorUnitario'].min(), df['valorUnitario'].max())

            plt.plot(df['data'], df['valorUnitario'], marker='o', linestyle='-')
            plt.title('Variação do Custo do Produto' + produto)
            plt.xlabel('Data')
            plt.ylabel('valorUnitario')
            plt.grid(True)
            plt.tight_layout()


            plt.savefig("D:\\"+produto+".png", dpi=300, bbox_inches="tight")
        except:
            print("Erro ao gravar imagem do gráfico")



    def calcular_variacao(valor_anterior, valor_atual):
        return ((valor_atual - valor_anterior) / valor_anterior) * 100


    def variacoesCincoPorcento():

        excluir_fornecedor = "xxxxxxxxxxxxxxxxxx"
        produtos_variacao_acima_5 = {}

        for produto, ocorrências in produtos.items():
            # Filtra as ocorrências para excluir o fornecedor especificado
            ocorrências_filtradas = [ocorr for ocorr in ocorrências if ocorr["fornecedor"] != excluir_fornecedor]

            ocorrências_filtradas = sorted(ocorrências_filtradas, key=lambda x: x['data'])  # Ordena as ocorrências filtradas pela data

            for i in range(1, len(ocorrências_filtradas)):
                valor_anterior = ocorrências_filtradas[i-1]['valorUnitario']
                valor_atual = ocorrências_filtradas[i]['valorUnitario']

                valor_anterior=valor_anterior.replace(",",".")
                valor_atual=valor_atual.replace(",",".")

                variacao = calcular_variacao(float(valor_anterior), float(valor_atual))

                if abs(variacao) > 5:  # Variação (positiva ou negativa) acima de 5%
                    if produto not in produtos_variacao_acima_5:
                        produtos_variacao_acima_5[produto] = []
                    produtos_variacao_acima_5[produto].append(ocorrências_filtradas[i])
                    nomeProduto=sanitize_filename(produto)
                    graficoCustoProduto(nomeProduto)



        # Converta o dicionário em uma lista de registros para o DataFrame
        records = []
        for produto, ocorrências in produtos_variacao_acima_5.items():
            for ocorr in ocorrências:
                records.append({"Produto ": produto, **ocorr})

        # Crie um DataFrame a partir dos registros
        df = pd.DataFrame(records)

        # Grave o DataFrame em um arquivo Excel
        df.to_excel("D:\\produtos_variacao_acima_5.xlsx", index=False, engine='openpyxl')


    origem = entrada_btn_arquivo.get()
    destino = entrada_btn_arquivo2.get()


    if not origem or not destino:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    if not destino.lower().endswith('.xlsx'):
        messagebox.showwarning("Atenção", "O arquivo do relatório resumido deve ter a extensão '.xlsx'.")
        return


    try:

        with open(destino, mode='w', newline='') as file:
            # Cria um objeto writer para escrever no arquivo CSV
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["FORNECEDOR","CNPJ/CPF","CODIGO PROD.", "DESCRICAO", "VR. UNITARIO", "QTD","UN.MEDIDA", "VR. TOTAL","ICMS SUBSTITUIÇÃO","FCOP","vICMSDeson","IPI","DESCONTO","SEGURO","FRETE","OUTRAS DESPESAS","CUSTO DO ITEM","CST","CFOP","NCM","NFE","ALIQUOTA","IMPOSTO","VR. LIQ. NFE","DATA ENTRADA","CHAVE ELETRONICA","vBCSTRet","pST","vICMSSubstituto","vICMSSTRet","pRedBCEfet","vBCEfet","pICMSEfet","vICMSEfet"])
            ler_todos_arquivos_xml(origem)
    except:
        print("Final da lista. Caso o resultado não esteja ok, verifique os caminhos constantes no arquivo empresas.csv!")

    for produto, ocorrencias in produtos.items():
        if len(ocorrencias) > 1:
            print(f"{produto} tem {len(ocorrencias)} ocorrências:")
            for ocorr in ocorrencias:
                pass






# Criação da janela principal
janela = tk.Tk()
janela.title("Processamento de Vendas - Cupom Eletrônico")


# Bloquear a janela para que não possa ser maximizada
janela.resizable(False, False)
source_var = tk.StringVar()
destination_var = tk.StringVar()

# String base64 do ícone .ico
icon_base64 = 'AAABAAEAgIAAAAEAIAAoCAEAFgAAACgAAACAAAAAAAEAAAEAIAAAAAAAAAABADjsAAA47AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBEAIRgPACEWEgAhFxEAIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBAAIRcPACEhEgAgFxEAIhcNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8XEAAfGBAAGBURABwWEAAgGBACIBgQBCAYEAIeEw8AHxMPACEbEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGRAAIBkQACEZEAEgGBAEIBgQAx8YEAEgGBAAIBgQAB4YEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhFxAAIBkQACAYEAAgGBACIBgQAyAXEAAgGBAAIBgPAB8YDwYgGBARIBgQECAYEBAgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBAQIBgQESAYEBAgGBALIBkWASAaFwAhGA4AIRgPASAYEAMfGBABIBgQACAYEAAdGQ4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACEXDwAhFw8AIBgQAyAYEAEiGBAAIBgQJSAYEHggGBC3IBgQ3SAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDvIBgQ7iAYEOUgGBDOIBgQnyAYEFIfGBAKHxgRACAYEAIgGBACIBgQACAYEAAgGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgFw8AIBcPACAYEAMgGBAAIBgQISAYEKYgGBD6IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEOEgGBBmHxcPAiAYEQEgGBACIBgQACAYEAAgGBEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhFxAAAC0kACEYDwAgGBADIBgQACAYEFsgGBDzIBgQ/yAYEP0gGBD7IBgQ/CAYEP0gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/SAYEPsgGBD8IBgQ/iAYEP8gGBC9IBgQGB8XEQAgGBACIBgQACAYEAAeGQ8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFxELACAYEAAgHRIAIBgQAyAYEAAgGBBzIBgQ/yAYEP0gGBD7IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD9IBgQ+iAYEP8gGBDcIBgQISAYEAAgGBACIBgQACAYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfGBAAHxkRACAYEAMgGBAAIBgQXSAYEP8gGBD7IBgQ/SAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ+iAYEP8gGBDSIBgQDyAZEAAgGBABIBgQACIUEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgGBACIBgQACAYECUgGBDwIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ+iAYEP8gGBCcIBgQACAZEAIhFxAAIBgPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhFxAAHhcQACEYEAIhGBAAIBgQpCAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD8IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBA7IBgQACAYEAIhGREAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACIYEAAgGBACIBgQACAYECcgGBD4IBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/iAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD9IBgQ7iAYEO8gGBDvIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7yAYEO4gGBDvIBgQ+iAYEP8gGBD9IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYEKYgGBAAIBgQAyAYDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRUQACAYEAQgGBAAIBgQdiAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEPcgGBAsIBgQCiAYEBIgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBAkIBgQgSAYEPggGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ7CAYEBYgGBAAIBgQAR8ZEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhGBAAHxgQAh8YEAAgGBC2IBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYENsgGBDsIBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEEcgGBAAIBgQAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBYRACAYEAMgGBAAIBgQVSAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQSiAYEAAgGBADIBcPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEfGA8AHhgPBSAYENkgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQTCAYELcgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQfCAYEAAgGBAFIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQAiAYEAUgGBAAIBgQsiAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBB/IBgQACAYEAQeGREAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBAOIBgQ6iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEPciGQ4JIBgQjSAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBCuIBgQACAYEAMgGBEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEQAZERsAIBgQBCAYEAAgGBBoIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYELMgGBAAIBgQAyAYDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ8iAYDwIgGBBYIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYENsgGBEGIBgRACAYEAErFRUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAXEAAgGBADIBgQACAXEDYgGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQ4CAYEAkgGBAAIBgQASYiCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQECAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDxIBgQByAYECkgGBD/IBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ+yAXECcgGBAAIBgQAh8YEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRsPACAYEAEgGBAAIBgQECAYEOogGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBD+IBgQLSAYEAAgGBACHhcRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO8gGBAOIBkPBCAYEOEgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQVSAYEAAgGBADIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACAYEAEgGBAAIBgQwiAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBBeIBgQACAYEAQgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7yAYEBMgGBAAIBgQtSAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBCJIBgQACAYEAQgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgFxAAIBgQBCAYEAAgGBCQIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEJQgGBAAIBgQBCAZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDvIBgQFSAYEAAgGBCBIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYELsgGBAAIBgQAiAYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8ZEQAgGBAEIBgQACAYEFogGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQxyEXEAAhFxABIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBAUIBgQACAYEE0gGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQ5B8YDwsfGA8AIBgQARoYFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRcQACAYEAIgGBAAIBgQKyAYEP0gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQFCAYEAAgGBABIRcOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBIgGBAAIBgQISAYEPcgGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQMSAYEAAgGBACIRkOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeFw8AIBgQASEYEAAhGBAIIBgQ3iAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBA9IBgQACAYEAMcFhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGRECIBgQ0yAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBBgIBgQACAYEAQgGBEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAIBgQAyAYEAAgGBCyIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEHAgGBAAIBgQBCQaEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAAgGBCjIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEJUgGBAAIBgQBCAZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAZEAAgGBAEIBgQACAYEH8gGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQpiAYEAAgGBADIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgFxAAIBgQACAYEG0gGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQxyEXEAAhFxABIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxgRACAYEAMgGBAAIBgQTCAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDVHhcSAx8XEQAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBAAIBgQOyAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBDtIBgQEyAYEAAgGBABHxgUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGRAAIBgQAiAYEAAgGBAgIBgQ9yAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEPggGBAjIBgQACAYEAIhGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAAgGBATIBgQ7SAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBA6IBgQACAYEAMfGQsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBcPACAWDgIgGBDTIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYEFEgGBAAIBgQAyAZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAiAZEAAgGBDFIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEGwgGBAAIBgQBCEZEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgGBADIBgQACAYEKQgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQhSAYEAAgGBAEHxgPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBAFIBgQACAYEJMgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQoSAYEAAgGBADIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxgQACAYEAQgGBAAIBgQbyAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBC5IBgQACAYEAIgGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAUgGBAAIBgQXSAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDQLAgZABwdDQAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfFBIAIBgQAyAYEAAgGBA8IBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEOMgGBALIBgQACAYEAEkGQ4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAyAYEAAgGBAtIBgQ/iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEPUgGRAcIBgQACAYEAIhGA8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAbDwAgGBABIBgQACAYEBUgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEDEgGBAAIBgQAh4XEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBACIBgQACAYEAkgGBDgIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEEYgGBAAIBgQAx8ZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEYDwAeGREBHxkRACAYEMggGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQYyAYEAAgGBAEIRgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEgGBADIBgQACAYELQgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQeCAYEAAgGBAEIhgPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACAYEAQgGBAAIBgQliAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBCYIBgQACAYEAMgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQASAYEAQgGBAAIBgQgCAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBCsIBgQACAYEAMgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAIBgQBCAYEAAgGBBhIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEMsdGBIAGxgTACEYDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABIBgQAyAYEAAgGBBMIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYENkfGBAFHxgQACAYEAEkJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEYDwAgGBACIBgQACAYEDAgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ8SAYEBggGBAAIBgQASAXEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEgGBACIBgQACAYECAgGBD3IBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ+iAYECUgGBAAIBgQAiAYEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHRoWACAYEAEhGBAAIRgQCyAYEOMgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQQiAYEAAgGBADIRYQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQASAYEAEgGREAIBkSASAYENMgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQUiAYEAAgGBADIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRcQACAYEAIgGBAAIBgQuSAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBB1IBgQACAYEAQeFw8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABIBgQACAYEAMgGBAAIBgQoyAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBCGIBgQACAYEAQgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhGQ8AIBgQBCAYEAAgGBCHIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYEKsgGBAAIBgQAyAYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEeFxAAIBgQBCAYEAAgGBBtIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYELggGBAAIBgQAiAXEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEXEAAgGBADIBgQACAYEFIgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQ2SAXEAUgFxAAIBgQAR4eDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQASEcEAAgGBADIBgQACAYEDsgGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQ4iAYEAogGBAAIBgQASgOCQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgRACAYEAIgGBAAIBgQJSAYEPkgGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBD6IBgQJiAYEAAgGBACIRcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABIRYQACAYEAEgGBAAIBgQEyAYEO0gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBD/IBgQLyAYEAAgGBACIBoRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAArKwAAIBgQAR8YEQAfGBIFIBgQ2CAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBBVIBgQACAYEAMgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAIBgQACAZEAEgGRAAIBgQxSAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBBeIBgQACAYEAQfGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfGBAAIBgQAyAYEAAgGBCqIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEIsgGBAAIBgQBCEYDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAgGRAAIBgQBCAYEAAgGBCTIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEJMgGBAAIBgQBCAZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEVDQAgGBAEIBgQACAYEHUgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQviAYEAAgGBACIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAB8YEAAgGBAEIBgQACAYEF0gGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQxSAYDwAfGA8BIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxkTACAYEAMgGBAAIBgQQyAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBDnIBgQDiAYEAAgGBABHhgRAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAIRgQACAYEAIgGBAAIBgQLSAYEP4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDrIBgQEiAYEAAgGBABHRQPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgFxAAIBgQASAYEAAgGBAaIBgQ8yAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBA1IBgQACAYEAMgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAVEgoAIBgQASAYEAAgGBAJIBgQ4CAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBA4IBgQACAYEAMfGhMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAHhkUAB8YEgAgGBDNIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEGggGBAAIBgQBCAXDwAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAfGQ8AIBgQAyAYEAAgGBC0IBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEGogGBAAIBgQBCIZDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgGBADIBgQACAYEJwgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQnSAYEAAgGBADIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAACEYEQAgGBAEIBgQACAYEIAgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQniAYEAAgGBADIBcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHhkRACAYEAQgGBAAIBgQZyAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDOIRUKABkzSAAgGBEAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAHxkPACAYEAMgGBAAIBgQTCAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDOJBEQAFMAEQAgGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhGQ8AIBgQAyAYEAAgGBA1IBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEPQgGBAcIBgQACAYEAIgFxEAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAgGBAAIBgQAiAYEAAgGBAgIBgQ9yAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEPMgGBAbIBgQACAYEAIhFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEVDgAgGBABIBgQACAZEA8gGBDoIBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEEcgGBAAIBgQAyEZEAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAgGBABIBkRACAZEgEgGBDTIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEEQgGBAAIBgQAx8XFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8YEAAhGBACIRgQACAYEMAgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQeyAYEAAgGBAEIBYRAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAACAYEAAgGBADIBgQACAYEKMgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQdiAYEAAgGBAEIRcMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxkQACAYEAQgGBAAIBgQjiAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBCvIBgQACAYEAMhGBAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAHhcQACAYEAQgGBAAIBgQbSAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/CAYEP8gGBCqIBgQACAYEAMgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAIBgQAyAYEAAgGBBZIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEN0iFw8HIRcPACEYEAEXEgwAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAhHBAAIBgQAyAYEAAgGBA7IBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYENceFhEEHxYRACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAZDwAgGBACIBgQACAYECogGBD8IBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ/CAYECogGBAAIBgQAiAZEAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAACEWEAAgGBABIBgQACAYEBMgGBDtIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ+SAYECQgGBAAIBgQAiEYEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHRQUACAYEAEgGBAAIBgQByAYEN0gGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQWiAYEAAgGBAEIBcQAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAACAYEAAgGRABIBkQACAYEMUgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEPwgGBD/IBgQUCAYEAAgGBADIRgPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxcQACAYEAMgGBAAIBgQsSAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBCQIBgQACAYEAQfGBAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAIBkQACAYEAQgGBAAIBgQkyAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBCEIBgQACAYEAUgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQBSAYEAAgGBB+IBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYEMMgGBAAIBgQASAYEAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAfGBAAIBgQBCAYEAAgGBBdIBgQ/yAYEPwgGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYELYgGBAAIBgQAiEZDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBADIBgQACAYEEggGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ6yAYEBIgGBAAIBgQAR8YEgAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAACEYEAAgGBACIBgQACAYEC0gGBD+IBgQ/yAYEP4gGBD/IBgQ/yAYEP0gGBD/IBgQ4iAYEBkgGBAOIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBIgGBAKIBgQLCAYEPcgGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQOSAYEAAgGBADHhkQAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAFRIKACAYEAEgGBAAIBgQCSAYEOAgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ8CAYEO4gGBDvIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO8gGBDuIBgQ/SAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBBsIBgQACAYEAQhFg8AAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAHxkPACAYEAMgGBAAIBgQtCAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEKIgGBAAIBgQAyAYEAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAhGBEAIBgQBCAYEAAgGBCAIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQ0hgfGQEeGhMAIBgQAQAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAB8ZDwAgGBADIBgQACAYEEwgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBDzIBgQGiAYEAAgGBABAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACAYEAIgGBAAIBgQICAYEPYgGBD/IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEPMgGBAaIBgQACAYEAEAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACAZEQEgGREAIBgQwCAYEP8gGBD5IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEPkgGBD/IBgQwB8YEQAfGBEBIBgQAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAiGhAAIBgQAiAYEAAgGBA6IBgQ9yAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEPcgGBA7IBgQACAYEAIhGQ8AAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAXDwAfFw4AIBgQAiAYEAAgGBA0IBgQuSAYEOkgGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7yAYEOogGBC6IBgQNSAYEAAgGBACHxcRACAXEAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgPACAYEAAgGBAAIBgQAiAYEAAgGBgAIBgODCAYEBEgGBAQIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBAgGBARIBcQDCEtAAAgGBAAIBgQAiAYEAAgGBAAIBgOAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgRACAYDwAgGA8AIBgQAyAYEAIgGBAAIRgPAB4aEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxoRACAYEAAgGBAAIBgQAiAYEAMgGBAAIBgQACAYEAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHxgRACAYEAAgGBAAIBgQACAYDwEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBAAIBgPACAYEAAiFxEAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzAAAAIBkQACQfDgAkGQ4AIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEhGBAAIRgPACEYDwAfFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGhQNACAYEAAgGBAAIBgQASAYEAMeFxEAHxcQAB8XEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkYFQAiGA8AIhgPACAYEAMgGBACIBgPACAYDwAhFxEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwcEwAgGBAAIBgQACAYEAEhGBACIBgQACEYEAYgGBARIBgQECAYEBAgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQECAYEBEgGBALIBgSAB8YEAEgGA8BIBgPACAYDwAeFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQACAYEAAgGBABlQATACAXEQogGBCFIBgQ3iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7yAYEOggGBCxIBgQKSAYDwAgGBACIRgQACEYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEQAgFxEAIBgQASAYEQEgGA4DIBgQtiAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBDsIBgQKiAYEAAgGBACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgFxEAIRgOAB8YEgAgGA8EIBgPACAYEJYgGBD/IBgQ+SAYEP0gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ+CAYEP8gGBCsIBgQACAYEAIhFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBkPACAYEAAhGQ8AIBgQBCAYEAAgGBByIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEOUgGBAMIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQXEgAgGBAAIBgQACAYEAQgGBAAIBgQTiAYEP8gGBD9IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ5iAYEAwgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAIBgQACAYEAAgGBADIBcQACAXEC4gGBDwIBgQ/yAYEP0gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ+CAYEP8gGBCsIBkQACAZEAIhFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgGBAAIBgQAiAYEAAgGBAWIBgQ2iAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ7CAYECsgGBAAIBgQAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQESAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDuIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBAAIBgQACAYEAEhGQ8BHxgRBCAYELsgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/SAYEP4gGBDyIBgQ7iAYEO8gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDvIBgQ6SAYELEgGBAqIBgQACAYEAIhGBAAIBcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO4gGBARIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQAB8ZDwAhFxAAIBgQAx8ZEAAgGBCZIBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQvCAYEBEgGBAQIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQECAYEBEgGBALJB0LACEZDwEgGBABIBgQACAYEAAfFhIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEBEgGBDuIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ7iAYEBEgGBAAIBgQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8YEAAgGBAAIRgQACAYEAQgGBAAIBgQdCAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD8IBgQ/yAYENsgGA8XIBgQACAYEAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfIAwAIBYRACAXEQAgGBADIBgQAiAYEAAgGBAAIBcRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEgGBAAIBgQECAYEO4gGBD/IBgQ/iAYEP8gGBD/IBgQ/iAYEP8gGBDvIBgQESAYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfGxAAIBgQACAYEAAgGBAEIBgQACAYEFAgGBD/IBgQ/SAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/iAYEP8gGBDyIBgQMSAYEAAgGBAEIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAXEQAfFxIAIBcRACIWDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBgQASAYEAAgGBARIBgQ7iAYEP8gGBD+IBgQ/yAYEP8gGBD+IBgQ/yAYEO8gGBARIBgQACAYEAEfFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRoNACAYEAAgGBAAIBgQAyAYEAAgGBAwIBgQ8SAYEP8gGBD+IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD9IBgQ/yAYEFEgGBAAIBgQBCAYEAAgGBAAIRURAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGBABIBgQACAYEA4gGBDqIBgQ/yAYEP4gGBD/IBgQ/yAYEP4gGBD/IBgQ8yEYDxohGA8AIRgPASAYEAAgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgFxAAIBcQACAYEAIgGBAAIBgQFyAYENsgGBD/IBgQ/CAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBB2IBgQACAYEAQgGhIAIBgQAB8XDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAEfGA8AHhgPBSAYENkgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP0gGBD/IBgQUSAYEAAgGBAHIBgPASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBACIhkRAR4YDwUgGBC+IBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQmyEYEAAgGBADHxkQACEXEAAgGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRcQACAYEAIgGBAAIBgQtiAYEP8gGBD8IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDTIRkQESEYEAAgGBABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBcQACAYEAEfGBAAIBgQnCAYEP8gGBD7IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEL0eGA8FIhgRASAYEAEgGA8AIBgPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhFRAAIBgQBCAYEAAgGBB2IBgQ/yAYEPsgGBD/IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDUIBgQTSEYDxYgGBAQIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBATIBkRBSAYEHkgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/SAYEP8gGBDbIBgQGCAXEAAgGBACIBgQACAYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEYDwAgGBACIBgQACAYECcgGBD4IBgQ/yAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/iAYEP4gGBD/IBgQ9CAYEO4gGBDvIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7yAYEO8gGBDuIBgQ/CAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD/IBgQ8iAYEDEgGBAAIBgQAyAYEAAgGBAAIxUOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRcQAB8YEAAhGBACIRgQACAYEKQgGBD/IBgQ+yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/SAYEPwgGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD9IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/SAYEP8gGBBSIBgQACAYEAQgGBAAIBgQACAbEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRgQACAYEAIgGBAAIBgQJSAYEPAgGBD/IBgQ/SAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEPsgGBD/IBgQeCAYEAAgGBAEIBkRACAYEQAgFxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfGBAAHxkRACAYEAMgGBAAIBgQXSAYEP8gGBD7IBgQ/SAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD7IBgQ/yAYEJ0fFhEAHxcQAyEZDwAgGBEAIRgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkTCwAfGRAAIh4RACAYEAMhGBAAIBgQcyAYEP8gGBD9IBgQ+yAYEP4gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ+yAYEP8gGBC/IRgRBR4YDwEgGBABIBgQACAYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEYEAAALkgAIhgPACAYEAMgGBAAIBgQWyAYEPMgGBD/IBgQ/SAYEPsgGBD8IBgQ/SAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEP4gGBD+IBgQ/iAYEPogGBD/IBgQ3CAYEBkgGBAAIBgQAiAYEAAhGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8YEAAfGA8AHxgPACAYEAMgGBAAIBgQICAYEKYgGBD6IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD/IBgQ/yAYEP8gGBD+IBgQ/yAYEO8gGBAyIBgQACAYEAMgGBAAIBgQACAaEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAYEAAgGA8AIBkPACAYEAMhGBABIRkPACAYECYgGBB5IBgQuCAYENsgGBDqIBgQ7yAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7iAYEO4gGBDuIBgQ7yAYEOkgGBCyIBgQKyAYEAAgGBADIBgQACAYEAAkHAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAZEAAgGBAAIBgQACAYEAIgGBADIBgQAB8ZEAAfGRAAIRcPBSAYEA4gGBARIBgQECAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBEgGBARIBgQESAYEBAgGBARHxgQCyMcDAAhGBABIBgQAiAYEAAgGBAAIBgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEXDwAfGBAAGBYTABwWEQAgGBACIBgQBCAYEAIkFwwAJhYLAB4YEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAICAWACAWDwAgFw8AIBkQAyAYEAIgGBAAIBgQAB8YEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIRgRACIYDgAAByoAIRgQACAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgGBABIBgQASAYEAEgFxAAHxcQACAXEAAiFg8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wAAAAAAAAAAAAAAB/////Qn/////////////6F////JQAAAAAAAAAAAAAAMX///ogAAAAAAAAAAAAAAAS///0gAAAAAAAAAAAAAAAAX//6QAAAAAAAAAAAAAAAAK//+oAAAAAAAAAAAAAAAABX//UAAAAAAAAAAAAAAAAAJ//yAAAAAAAAAAAAAAAAACP/8gAAAAAAAAAAAAAAAAAT/+QAAAAAAAAAAAAAAAAAE//kAAAAAAAAAAAAAAAAAAv/5AAAv////////////kAJ/+gAAIAAAAAAAAAAAAAgCf/oAACf///////////+oAn/6AAAX////////////yAF/+gAAF////////////+gBf/oAABP////////////kAT/6AEAT////////////5AE/+gBAE////////////+QBP/oAQAv////////////0AL/6AEAL////////////9AC/+gBACf////////////IAn/oAYAn////////////yAJ/6AGAJ////////////8gBf+gBgBf////////////oAX/oAYAX////////////6AE/6AFAE////////////+QBP+gBQBP////////////kAT/oAUAb////////////9AC/6AFAC/////////////QAv+gBQAv////////////yAJ/oASAJ////////////8gCf6AEgCf////////////IAn+gBIAX////////////6AF/oASAF////////////+gBf6AEgBP////////////kAT+gBEAT////////////5AE/oARAE////////////+QAv6AFQAv////////////0AL+gBUAL////////////9ACfoAUgCf////////////IAn6AFIAn////////////yAJ+gBSAJ////////////+gBfoAWgBf////////////oAX6AFoAX////////////5AE+gBZAE////////////+QBPoAWQBP////////////kAb6AFkAT////////////9AC+gBdAC/////////////QAnoAXQAv////////////yAJ6AFyAJ////////////8gCegBcgCf////////////IAXoAXoAX////////////6AF6AF6AF////////////+gBOgBeQBP////////////kAToAXkAQAAAAAAAAAAAABAE6AF5AE/////////////QAugBfQAAAAAAAAAAAAAAAALoAX0AAAAAAAAAAAAAAAACaAF8gAAAAAAAAAAAAAAAAmgBfIAAAAAAAAAAAAAAAAFoAXyAAAAAAAAAAAAAAAABaAF+gAAAAAAAAAAAAAAAAWgBfkAAAAAAAAAAAAAAAAJoAX5AAAAAAAAAAAAAAAACaAF+oAAAAAAAAAAAAAAABWgBf0gAAAAAAAAAAAAAAALoAX8l//////////////+k6AF/0AAAAAAAAAAAAAAAC+gBf//////////////////oAX//////////////////6AF//////oAAAAAAAAC//+gBf/////0X///////6X//oAX/////6QAAAAAAAAS//6AF/////9QAAAAAAAABX/+gBf////+gAAAAAAAAAL//oAX/////CAAAAAAAAACf/6AF/////1AAAAAAAAAAX/+gBf////6gAAAAAAAAAF//oAX////9QAAAAAAAAACf/6AF////+oAAAAAAAAAAv/+gBf////QAAAAAAAAAAV//oAX////hAAAAAAAAAAS//6AF////6gAX///////pf/+gBf///9QAIAAAAAAAAv//oAX///+oAFf//////////6AE////UACv//////////+gBAAAAAABD///////////kAL///8gAF///////////5AAAAAAAAK///////////+QAAAAAAAFf///////////yAAAAAAACv///////////8gAAAAAABX////////////UAAAAAAAh////////////6gAAAAAAC////////////+kAAAAAAFf////////////0gAAAAACv////////////+iAAAAABX/////////////yUAAAABL//////////////Qn///+k///////////////gAAAAC//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8='

# Decodifica a string base64
icon_data = base64.b64decode(icon_base64)
icon_image = Image.open(BytesIO(icon_data))

# Converte a imagem para um PhotoImage
icon_photo = ImageTk.PhotoImage(icon_image)

# Define o ícone da janela
janela.iconphoto(True, icon_photo)    







'''
janela.title("Seleção de Arquivo e Diretório")

# Botão para selecionar o arquivo CSV
btn_arquivo = tk.Button(janela, text="Selecionar diretório XML", command=selecionar_caminho_xml)
btn_arquivo.pack(pady=5)

# Label para mostrar o arquivo selecionado
label_arquivo = tk.Label(janela, text="Nenhum diretório selecionado")
label_arquivo.pack()
'''


tk.Label(janela, text="Selecionar Diretório - XML").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entrada_btn_arquivo = tk.Entry(janela, width=50)
entrada_btn_arquivo.grid(row=0, column=1, padx=10, pady=5)
btn_arquivo = tk.Button(janela, text="Selecionar", command=selecionar_caminho_xml)
btn_arquivo.grid(row=0, column=2, padx=10, pady=5)


tk.Label(janela, text="Arquivo para salvar o relatório resumido (.xlsx):").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entrada_btn_arquivo2 = tk.Entry(janela, width=50)
entrada_btn_arquivo2.grid(row=1, column=1, padx=10, pady=5)
btn_arquivo2 = tk.Button(janela, text="Selecionar", command=selecionar_caminho_relatorio)
btn_arquivo2.grid(row=1, column=2, padx=10, pady=5)



# Botão para executar a função

btn_executar = tk.Button(janela, text="Executar", command=executar, width=20, bg='green', fg='white')
btn_executar.grid(row=3, column=1, padx=10, pady=20)

# Inicia o loop da interface
janela.mainloop()
