import xml.etree.ElementTree as ET
import csv
import os
import pandas as pd

produtos = {}

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
            vICMSDeson= 0# ICMSTot.find('./nfe:vICMSDeson', namespace).text #evita erros na gravação
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
            vFCPST= 0# ICMSTot.find('./nfe:vFCPST', namespace).text #evita erros na gravação
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
    
    for items_det in det:
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


            
            if(float(vDesc)>0):
                descontoRateaItem= (float(vDesc)/float(vProdTOTAL))* float(valor) 
                descontoRateaItem=descontoRateaItem
                descontoRateaItem="-" + str(descontoRateaItem)
                descontoRateaItem=str(descontoRateaItem).replace('.',',')                
            
            else:
                descontoRateaItem=0
            
            if(float(vFrete)>0):
                freteRateado= (float(vFrete)/float(vProdTOTAL))* float(valor) 
                freteRateado=freteRateado
                freteRateado=str(freteRateado).replace('.',',')                
            
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
            custoTotaldoItem= float(valor)+ ((float(vFrete)/float(vProdTOTAL))* float(valor) ) + ((vIPI_arredondado/float(vProdTOTAL)) * float(valor) ) + ((vST_arredondado/float(vProdTOTAL)) * float(valor)) - ((float(vDesc)/float(vProdTOTAL))* float(valor)) +(float(vOutro)/float(vProdTOTAL))* float(valor) 
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
            vFrete= 0#evita erros na gravação
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
    invalid_chars = '<>:"/\|?*'
    
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

        
        plt.savefig("C:\\Users\\Gabriel\\Desktop\\chromedriver_win32\\testexml\\graficos\\"+produto+".png", dpi=300, bbox_inches="tight")
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
    df.to_excel("C:\\produtos_variacao_acima_5.xlsx", index=False, engine='openpyxl')



caminhoListaEmpresas='C:\\Users\\Gabriel\\Desktop\\chromedriver_win32\\leitorXML4.0\\empresas.csv'  # O ARQUIVO empresas.CSV tem que ficar no mesmo diretório do scritp lendoXMLCompleto4.0.py
                                                                                                    # Nesse arquivo é para constar a origem dos arquivos XML e o destino do relatório que será salvo

with open(caminhoListaEmpresas) as f:
    next(f)        #pula o cabeçalho
    
    for line in f:
        
        line=line.strip()
        line=line.split(";")
        
        origem= line[1]
        destino=line[2]

        try:

            with open(destino, mode='w', newline='') as file:
                # Cria um objeto writer para escrever no arquivo CSV
                writer = csv.writer(file, delimiter=';')
                writer.writerow(["FORNECEDOR","CNPJ/CPF","CODIGO PROD.", "DESCRICAO", "VR. UNITARIO", "QTD","UN.MEDIDA", "VR. TOTAL","ICMS SUBSTITUIÇÃO","IPI","DESCONTO","SEGURO","FRETE","OUTRAS DESPESAS","CUSTO DO ITEM","CST","CFOP","NCM","NFE","ALIQUOTA","IMPOSTO","VR. LIQ. NFE","DATA ENTRADA","CHAVE ELETRONICA","vBCSTRet","pST","vICMSSubstituto","vICMSSTRet","pRedBCEfet","vBCEfet","pICMSEfet","vICMSEfet"])
                ler_todos_arquivos_xml(origem)
        except:
            print("Final da lista. Caso o resultado não esteja ok, verifique os caminhos constantes no arquivo empresas.csv!")

        for produto, ocorrencias in produtos.items():
            if len(ocorrencias) > 1:
                print(f"{produto} tem {len(ocorrencias)} ocorrências:")
                for ocorr in ocorrencias:
                    pass
