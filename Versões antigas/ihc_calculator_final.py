
# ## Bibliotecas


import subprocess
import os
import sys
from osgeo import gdal
import rasterio
import numpy as np
import numpy.ma as ma
import tkinter as tk
from tkinter import filedialog
import shutil



#####################################################Interface Gráfica para selecionar o endereço dos arquivos utilizados pelo programa#########################################################################################

class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IHC - UFF")
        #self.root.geometry("500x600")

        # Variables to store file paths
        self.pits_removed_path = tk.StringVar()
        self.weighting_factor_path = tk.StringVar()
        self.ips_path = tk.StringVar()
        self.q_runoff_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_name=tk.StringVar()
        self.treshold=tk.StringVar()
           
        

        tk.Label(root, text="IHC Calculator", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Create labels
        tk.Label(root, text="Pits Removed DTM :").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        tk.Label(root, text="Weighting Factor :").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        tk.Label(root, text="IPS :").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        tk.Label(root, text="Q RunOff :").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        #tk.Label(root, text="Folder for the intermediate rasters").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        tk.Label(root, text="Output Path :").grid(row=7, column=0, sticky="e", padx=10, pady=5)

        # Create entry widgets to display selected file paths
        tk.Entry(root, textvariable=self.pits_removed_path, width=50, state='readonly').grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        tk.Entry(root, textvariable=self.weighting_factor_path, width=50, state='readonly').grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        tk.Entry(root, textvariable=self.ips_path , width=50, state='readonly').grid(row=3, column=1, columnspan=2, padx=10, pady=5)
        tk.Entry(root, textvariable=self.q_runoff_path, width=50, state='readonly').grid(row=4, column=1, columnspan=2, padx=10, pady=5)
        tk.Entry(root, textvariable=self.output_path, width=50, state='readonly').grid(row=7, column=1, columnspan=2, padx=10, pady=5)

        

        # Create browse buttons
        tk.Button(root, text="Open", command=lambda: self.browse_file(self.pits_removed_path, "Select Pits Removed DTM File")).grid(row=1, column=3, padx=10, pady=5)
        tk.Button(root, text="Open", command=lambda: self.browse_file(self.weighting_factor_path,"Select Weighting Factor File" )).grid(row=2, column=3, padx=10, pady=5)
        tk.Button(root, text="Open", command=lambda: self.browse_file(self.ips_path, "Select IPS File")).grid(row=3, column=3, padx=10, pady=5)
        tk.Button(root, text="Open", command=lambda: self.browse_file(self.q_runoff_path, "Select Q RunOff File")).grid(row=4, column=3, padx=10, pady=5)
        tk.Button(root, text="Open", command=self.browse_output_folder).grid(row=7, column=3, padx=10, pady=5)
        
        # Create checkbutton for deleting the process folder
        self.accept_check = tk.StringVar(value="Don't delete")
        self.acc_check = tk.Checkbutton(
            root,
            text="Delete Process Folder",
            variable=self.accept_check,
            onvalue="Delete process folder",
            offvalue="Don't delete"
        )
        self.acc_check.grid(row=9, column=1, columnspan=2, pady=10)
        
        # Create checkbox for choosing drainage or outlet
        self.en_trsh=tk.StringVar(value="outlet")
        self.enter_treshold_check = tk.Checkbutton(
            root,
            text="Check for drainage",
            variable=self.en_trsh,
            onvalue="drainage",
            offvalue="outlet",
            command=self.toggle_treshold_entry
        )

        self.enter_treshold_check.grid(row=5, column=1, pady=10, padx=20)

        # Create the treshold entry and label
        self.treshold_label = tk.Label(root, text="Enter the treshold :")
        self.treshold_entry = tk.Entry(root, textvariable=self.treshold, width=5, state='normal')
        self.treshold_label.grid(row=5, column=2, sticky="e", padx=10, pady=5)
        self.treshold_entry.grid(row=5, column=3, padx=10, pady=5)
        
        tk.Label(root,text="Outlet/Drainage :").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        
        #sep
        tk.Label(root, text="---------------------------------------------------------").grid(row=6,column=0,columnspan=4)

        # Rename the output
        tk.Label(root,text="Output Name :").grid(row=8, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(root, textvariable=self.output_name, width=50, state='normal').grid(row=8, column=1, columnspan=2, padx=10, pady=5)
        

        # Create OK button to confirm and close the window
        tk.Button(root, text="OK", command= self.root.destroy).grid(row=10, column=1, columnspan=2, pady=10)

        # Initialize the visibility of the treshold entry
        self.toggle_treshold_entry()
    
    def toggle_treshold_entry(self):
        if self.en_trsh.get() == "drainage":
            self.treshold_label.grid(row=5, column=2, sticky="e", padx=10, pady=5)
            self.treshold_entry.grid(row=5, column=3, padx=10, pady=5)
        else:
            self.treshold_label.grid_forget()
            self.treshold_entry.grid_forget()
 

    # Delete process folder
    def delete_process_folder(self):
        folder_path = processamento_path

        accepted = self.accept_check.get()
        if accepted == "Delete process folder":
            try:
                shutil.rmtree(folder_path)  # This removes the folder even if it's not empty
                print(f"Process folder '{folder_path}' has been deleted.")
            except Exception as e:
                print(f"Error deleting process folder: {e}")


            
    def browse_file(self, var,dialog_title):
        # Open file dialog and update the variable with the selected file path
        file_path = filedialog.askopenfilename(title=dialog_title)
        var.set(file_path)


    def browse_output_folder(self):

        # Open folder dialog and update the variable with the selected folder path
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        self.output_path.set(folder_path)

    

root = tk.Tk()
app = FileSelectorApp(root)
root.mainloop()

####################################################################Começando o cálculo do IHC###########################################################################################



driver = gdal.GetDriverByName("GTiff")


# ## Definicoes


driver = gdal.GetDriverByName("GTiff")



#Endereços dos rasters de entrada

dtm =  app.pits_removed_path.get()
weighting = app.weighting_factor_path.get()
IPS = app.ips_path.get()
q_run_off = app.q_runoff_path.get()

#Saida
endereco_saida = app.output_path.get()

#output name
output_name=app.output_name.get()+".tif"

#process folder
processamento_path = os.path.join(app.output_path.get(), f"process_of_{app.output_name.get()}")
os.makedirs(processamento_path, exist_ok=True)
endereco_processos = processamento_path


Pits_Removed_DTM = os.path.join(dtm)
Weighting_Factor = os.path.join(weighting)

Qrunoff = os.path.join (q_run_off)
IHC = os.path.join(endereco_saida, "ihc.tif")


with rasterio.open(Pits_Removed_DTM) as dataset:
    x_dim, y_dim = dataset.shape


print(x_dim)
print(y_dim)

# ## Calculos

# #### raster_comparison

#Function to compare two different rasters. We want to check if the raster generated by the algorithms are the same as the arcgis ones

def raw_raster_comparison (raster1, raster2):
   with rasterio.open(raster1) as src1, rasterio.open(raster2) as src2:
      data1 = src1.read(1)
      data2 = src2.read(1)
      nodata1 = src1.nodata
      nodata2 = src2.nodata

      # comparison = np.array_equal(data1, data2)
      comparison = np.isclose(data1,data2, rtol=1e-3)

      print (f'They are equal: {comparison}')
      print(f'nodata1: {nodata1}')
      print(f'nodata2: {nodata2}')

      return comparison
   
def raster_close_enough (raster1, raster2):
#raster 1 and raster 2 are the paths to the rasters
  with rasterio.open(raster1) as src1, rasterio.open(raster2) as src2:

      data_1,nodata1 = mascara(src1)

      data_2,nodata2 = mascara(src2)

      comparison = np.isclose(data_1,data_2, rtol=1e-3)
      # comparison = np.array_equal(data_1,data_2,)
      # diff = np.ma.subtract(data_1, data_2)

      # diferenca = np.ma.sum(diff)
      iguais = np.all(comparison)

      print (f'They are close enough: {iguais}')
      print(f'nodata1: {nodata1}')
      print(f'nodata2: {nodata2}')
      # print(f'element-wise difference: {diferenca}')


      return 



def raster_comparison (raster1, raster2):
    #raster 1 and raster 2 are the paths to the rasters
    with rasterio.open(raster1) as src1, rasterio.open(raster2) as src2:

        data_1,nodata1 = mascara(src1)

        data_2,nodata2 = mascara(src2)

        comparison = np.array_equal(data_1,data_2)

        print (f'They are equal: {comparison}')
        print(f'nodata1: {nodata1}')
        print(f'nodata2: {nodata2}')



#funcao para lidar com os valores de nodata

def mascara(src):
  data = src.read(1)
  data_nodata = src.nodata
  masked = data == data_nodata
  masked_data = np.ma.masked_array(data, mask=masked, fill_value=src.nodata)  # Set fill_value to nodata
  return masked_data, data_nodata

# Esta função recebe um raster aberto pelo rasterio.
# Ela primeiro lê os dados da primeira banda
# Em seguida salva o valor de no_data disponível nos metadados
# Cria uma máscara
# Aplica a máscara e define então um masked numpy array
# Ela devolve o masked numpy array e o valor do nodata (útil pra debugar)



# ### 2 - Computando Infinity Flow


#2 Computando Infinity Flow 
# Compute D-Infinity flow directions and slope
dtmfillokang_tif_path = os.path.join(endereco_processos, "dtmfillokang.tif").replace("\\", "/")
#print("VERIFICAR ESTE ENDERECO" + dtmfillokang_tif_path)
dtmfillokslp_tif_path = os.path.join(endereco_processos, "dtmfillokslp.tif").replace("\\", "/")


dtmfillokang_tif = driver.Create(dtmfillokang_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
dtmfillokslp_tif = driver.Create(dtmfillokslp_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64) 

dtmfillokang_tif = None
dtmfillokslp_tif = None

print("2 Computing D-infinity flow")
subprocess.run(["dinfflowdir","-ang", dtmfillokang_tif_path, "-slp", dtmfillokslp_tif_path, "-fel", Pits_Removed_DTM], check=True)



# #### Nodata_Normalisation


# ### 3 - D8Flow Directions

Pits_Removed_DTM = os.path.join(dtm)


#D8 Flow

# Process: D8 Flow Directions (D8 Flow Directions) ()
dtmfillokp_tif_path = os.path.join(endereco_processos, "dtmfillokp.tif").replace("\\", "/")
dtmfilloksd8_tif_path = os.path.join(endereco_processos, "dtmfilloksd8.tif").replace("\\", "/")
dtmfillokp_tif = driver.Create(dtmfillokp_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
dtmfilloksd8_tif = driver.Create(dtmfilloksd8_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

dtmfillokp_tif = None
dtmfilloksd8_tif = None


    # 3
subprocess.run(["d8flowdir", "-p", dtmfillokp_tif_path, "-sd8", dtmfilloksd8_tif_path, "-fel", Pits_Removed_DTM], check=True)
print('3 D8 Flow complete')
print("")



# ### 8 - D8 Contibuting Area

# Process: D8 Contributing Area (D8 Contributing Area) ()
fillad8_tif_path = os.path.join(endereco_processos, "dtmfillokad8.tif").replace("\\", "/")
fillad8_tif = driver.Create(fillad8_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

fillad8_tif = None

subprocess.run(["aread8","-p", dtmfillokp_tif_path, "-ad8", fillad8_tif_path,"-nc"], check=True)
print('D8 Contributing Area Complete')
print("")

# #### Finding out and selecting the outlet

#The outlet should have the highest accumulated value
target_tif_path = os.path.join(endereco_processos, "outlet.tif").replace("\\", "/")
target_tif = driver.Create(target_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
target_tif = None


t_tif_path = os.path.join(endereco_processos, "teste.tif").replace("\\", "/")
t_tif = driver.Create(target_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
t_tif = None

with rasterio.open(fillad8_tif_path) as src1 : 
    
    profile = src1.profile 

    values, nodata_value = mascara(src1)
    check=app.en_trsh.get()

    if check == "outlet":
        highest_value = values.max()
        values = ma.where(values==highest_value, 1, 0)
    else :
        highest_value = float(app.treshold.get())
        values = ma.where(np.greater(values,highest_value), 1, 0)
  
with rasterio.open(target_tif_path, 'w', **profile) as dst:
    dst.write(values, 1)
    print(dst.nodata)

# with rasterio.open(t_tif_path, 'w', **profile) as dst:
#     dst.write(values, 1)
#     print(dst.nodata)

print(" complete!")
print("")

# ### 9 - Accumulating W

# Process: accumulating W (D-Infinity Contributing Area) () #Verificar!
accW_tif_path = os.path.join(endereco_processos, "accW.tif").replace("\\", "/")
accW_tif = driver.Create(accW_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

accW_tif = None

subprocess.run(["areadinf","-ang", dtmfillokang_tif_path, "-sca", accW_tif_path, "-wg", Weighting_Factor, "-nc"],check=True)
print('Process: accumulating W  complete') 
print("")

# ### 5 - D Infinity Contributing Area


# Process: D-Infinity Contributing Area (D-Infinity Contributing Area) 
dtmfilloksca_tif_path = os.path.join(endereco_processos,"dtmfilloksca.tif").replace("\\", "/")
dtmfilloksca_tif = driver.Create(dtmfilloksca_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

dtmfilloksca_tif = None

#4
subprocess.run(["areadinf", "-ang", dtmfillokang_tif_path, "-sca", dtmfilloksca_tif_path, "-nc"], check=True)
print( '4 D-Infinity Contributing Area (D-Infinity Contributing Area) complete')
print("")


# ### 1 - Resolution - Raster Constante

#Criando o Raster constante
 # Process: Create Constant Raster (Create Constant Raster) (sa)
resolution_tif_path = os.path.join(endereco_processos,"resolution.tif").replace("\\", "/")
resolution_tif = driver.Create(resolution_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
resolution_tif = None

with rasterio.open (Pits_Removed_DTM) as molde:
            transform = molde.transform
            largura_pixel =  transform[0]
            
            dem_data = molde.read(1)
            dem_nodata = molde.nodata
            dem_profile = molde.profile

            mask =  dem_data == dem_nodata # está fazendo um array booleano marcando os lugares de nodata como True

            masked_dem =  np.ma.masked_array(dem_data, mask = mask)
            masked_dem [~mask] = largura_pixel #~ significa not, neste contexto. Isto é, modifica tudo que não é máscara.


 #Salvando o Raster Constante

with rasterio.open (resolution_tif_path, 'w', **dem_profile) as new_dst:
    new_dst.write(masked_dem, 1)
     



# ### 11 - Divide - Raster Calculator (OK)


#11 DIVIDE - RASTER CALCULATOR - OK
# Process: Divide (Divide) (sa)


ACCfinal_tif_path = os.path.join(endereco_processos,"ACCfinal.tif")
ACCfinal_tif = driver.Create(ACCfinal_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
ACCfinal_tif = None


with rasterio.open(dtmfilloksca_tif_path) as src1, rasterio.open(resolution_tif_path) as src2:
    # Read the data into NumPy arrays

    filloksca,filloksca_nodata = mascara(src1)
    resolution,resolution_nodata = mascara(src2)

    #Fazendo a divisão em si:

    # Check if the two raster datasets have the same shape
    if filloksca.shape == resolution.shape:
        # Perform the division operation
        divisao = ma.divide(filloksca, resolution)
        

        # Create a new raster dataset for the result
        profile = src1.profile  # Copy the profile from one of the input rasters
        
        # profile.update(nodata = result_nodata) #atualizando o perfil base para ter o no data value novo
        
        
        with rasterio.open(ACCfinal_tif_path, 'w', **profile) as dst:
            dst.write(divisao, 1)
            
            print('Divide complete')
    else:
        print("Raster datasets have different shapes.")


# ### 15 - CMEAN (OK)

#15 CMEAN

print ("")        
print("15 CMEAN")
print("")       
# Process: Computing C mean (Raster Calculator) (sa)
cmean_tif_path = os.path.join(endereco_processos,"cmean_2.tif")
cmean_tif = driver.Create(cmean_tif_path, x_dim, y_dim, 1, gdal.GDT_Float64)  # Use Float64 here

cmean_tif = None
print( "cmeantif created")
print("")

with rasterio.open(accW_tif_path) as src1, rasterio.open(Weighting_Factor) as src2, rasterio.open(ACCfinal_tif_path) as src3:
    # Read the data into NumPy masked arrays
    accw, accw_nodata = mascara(src1)
    wfactor, wfactor_nodata = mascara(src2)
    accfinal, accfinal_nodata = mascara(src3)
    
    print(accw_nodata)
    print(wfactor_nodata)
    print(accfinal_nodata)

    soma = ma.add(wfactor,accw)
    print ('Soma realizada!')
    # plt.imshow(result_sum)
    # plt.show()
    

    if accfinal.shape == soma.shape:
        # Perform the division operation
        cmean = ma.divide(soma, accfinal)
        print ('divisão realizada')
        
        # Create a new raster dataset for the result
        profile = src2.profile  # Copy the profile from one of the input rasters

        with rasterio.open(cmean_tif_path, 'w', **profile) as dst:
            dst.write(cmean, 1)
            print(f'cmean {dst.nodata}')
            print("Computing C mean operation completed.")
    else:
        print("Raster datasets have different shapes.")


# ### 6 - Imposing upper and lower limits
  
print("")
print("6 imposing upper and lower limits to the slope")
print("")
# Process: Imposing upper and lower limits to Slope (Raster Calculator) (sa)
s_tif_path = os.path.join(endereco_processos,"s.tif")
s_tif = driver.Create(s_tif_path, x_dim, y_dim, 1, gdal.GDT_Float64)

s_tif = None

with rasterio.open(dtmfilloksd8_tif_path) as src:
    profile = src.profile  # Get the raster profile (metadata)
    slope,slope_nodata = mascara(src)   # Read the raster data (assuming it's a single-band raster)
    # Apply upper and lower limits
    # print(data_nodata)
    slope = ma.where(slope > 1, 1, slope)
    slope = ma.where(((slope < 0.005) & (slope != slope_nodata)), 0.005, slope)


# Write the processed data to the output raster
with rasterio.open(s_tif_path, 'w', **profile) as dst:
    dst.write(slope, 1)
    print(f'dst_nodata {dst.nodata}')
print("imposing limits to slope complete!")
print("")


# ### 12 - accumulating S (D-Infinity Contributing Area)

# Process: accumulating S (D-Infinity Contributing Area) ()
print("12 D infinity contributing area")
print("")
accS_tif_path = os.path.join(endereco_processos,"accS.tif").replace("\\", "/")
accS_tif = driver.Create(accS_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

accS_tif = None

subprocess.run(["areadinf","-ang", dtmfillokang_tif_path, "-sca", accS_tif_path, "-wg", s_tif_path, "-nc"],check=True)

print("D infinity contributing areas complete!")
print("")

# ### 17 - Smean (OK)

#17 (OK)
#17 S Mean - OK
# Process: Computing S mean (Raster Calculator) (sa)
print("17 computing S mean")
print("")

smean_tif_path = os.path.join(endereco_processos,"smean.tif")
smean_tif = driver.Create(smean_tif_path, x_dim, y_dim, 1, gdal.GDT_Float64)  

smean_tif = None

with rasterio.open(accS_tif_path) as src1, rasterio.open(s_tif_path) as src2, rasterio.open(ACCfinal_tif_path) as src3:
    # Read the data into NumPy masked arrays
    accs, accs_nodata = mascara(src1)
    s, s_nodata = mascara(src2)
    accfinal, accfinalnodata = mascara(src3)

    # Perform the adding operation
    soma = ma.add(s,accs )
    

    if accfinal.shape == soma.shape:
        # Perform the division operation
        divisao = ma.divide(soma, accfinal)

        # Create a new raster dataset for the result
        profile = src1.profile  # Copy the profile from one of the input rasters

        with rasterio.open(smean_tif_path, 'w', **profile) as dst:
            dst.write(divisao, 1)  # Use filled() to handle masked values

            print(f'resultado_nodata: {dst.nodata}')
            print("Division operation completed.")
            print("")

    else:
        print("Raster datasets have different shapes.")

# ### 4 - Accumulating q


#4 
print("")
print("4 Acummulating q")  
# Process: Accumulating q (D-Infinity Contributing Area) () 
accq_tif_path = os.path.join(endereco_processos,"accq.tif").replace("\\", "/")
accq_tif = driver.Create(accq_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)

accq_tif = None
print("")
print("accq_tif created")
print("")
subprocess.run(["areadinf","-ang", dtmfillokang_tif_path, "-sca", accq_tif_path, "-wg", Qrunoff, "-nc"],check=True)

#10  transformacao - OK
# Process: unittransformation (Raster Calculator) (sa)
print("unit transformation")

qrunm_tif_path = os.path.join(endereco_processos,"qrunm.tif").replace("\\", "/")
qrunm_tif = driver.Create(qrunm_tif_path, x_dim, y_dim, 1, gdal.GDT_Float64)  

qrunm_tif = None

with rasterio.open(accq_tif_path) as src:
    profile = src.profile  # Get the raster profile (metadata)
    data,data_nodata = mascara(src)    # Read the raster data (assuming it's a single-band raster)
    result = data/1000 

   
with rasterio.open(qrunm_tif_path, 'w', **profile) as dst: #qrunm é o accq corrigido
    dst.write(result, 1)
print("Unit transformation complete!")
print("")


# ### 16 - IPS - Raster Calculator (OK)


# Process: IPSs (Raster Calculator) (sa)

print("starting IPS!")
print("")
IPSxQr_path = os.path.join(endereco_processos,"IPSxQr.tif").replace("\\", "/")
IPSxQr = driver.Create(IPSxQr_path, x_dim, y_dim, 1, gdal.GDT_Float64)  

IPSxQr = None

with rasterio.open(IPS) as src1, rasterio.open(qrunm_tif_path) as src2:
    profile = src1.profile  # Get the raster profile (metadata)
    
    ips, ips_nodata = mascara(src1)  
    qrunm, qrunm_nodata = mascara(src2)

    produto = ma.multiply(ips,qrunm)
    
# Write the processed data to the output raster
with rasterio.open(IPSxQr_path, 'w', **profile) as dst:
    dst.write(produto, 1)
    print(f'final: {dst.nodata}')
print("IPSs complete!")
print("")

# ### 19 - Computing Upslope Component - Raster Calculator (OK)
  
# Process: Computing Upslope Component (Raster Calculator) (sa)
print("starting computing upslope component")
print("")
Dup_tif_path = os.path.join(endereco_processos,"Dup.tif").replace("\\", "/")
Dup_tif = driver.Create(Dup_tif_path, x_dim, y_dim, 1, gdal.GDT_Float64)  

Dup_tif = None

with rasterio.open(cmean_tif_path) as src1, rasterio.open(smean_tif_path) as src2, rasterio.open(IPSxQr_path) as src3, rasterio.open(resolution_tif_path) as src4 :
    profile = src1.profile 
    
    cmean, cmean_nodata = mascara (src1)
    smean, smean_nodata = mascara (src2)
    IPSxQr, IPSxQr_nodata = mascara (src3)
    resolution, resolution_nodata = mascara (src4)
    
    upslope = cmean * smean * IPSxQr * resolution * resolution # Atenção, todos aqui são masked arrays, então não tem problema fazer o cálculo assim.    
    
with rasterio.open(Dup_tif_path, 'w', **profile) as dst:
    dst.write(upslope, 1)

print ("upslope component complete!")

# ### 7 - Reclassify (OK)

# Process: Reclassify (Reclassify) (sa)
print("")
print("7 reclassifying")
flowd8_path = os.path.join(endereco_processos,"flowd8.tif").replace("\\", "/")
flowd8 = driver.Create(flowd8_path, x_dim, y_dim, 1, gdal.GDT_Float64)  

flowd8 = None
with rasterio.open(dtmfillokp_tif_path) as src: #fillokp é o d8 directions
    d8dir,d8dir_nodata =  mascara(src)
    profile = src.profile
    

    reclassified_data = np.select(
        [d8dir == 1, d8dir == 2, d8dir == 3, d8dir == 4, d8dir == 5, d8dir == 6, d8dir == 7, d8dir == 8],
        [1, 128, 64, 32, 16, 8, 4, 2], default=d8dir
    )  
    
    reclassified_data = ma.array(reclassified_data, mask=ma.getmask(d8dir)) # fazendo com que ele volte a ser um masked array copiando a máscara do orignal
    

with rasterio.open(flowd8_path, 'w', **profile) as dst:
    dst.write(reclassified_data, 1)
    print(f'final: {dst.nodata}')
print("Reclassify complete!")
print("")


# ### 14 - Integrating Sinks - (OK)

# 14 VERIFICAR - OK, só muda o nome da variável mesmo.
# Process: Integrating Sinks and Targets into D8 Flow directions (Raster Calculator) (sa)
print("14 starting process of integrating sinks ")
print("")
flowdir_tif_path = os.path.join(endereco_processos, "flowdir.tif").replace("\\", "/")

with rasterio.open(flowd8_path) as src:
    profile = src.profile 
    data = src.read(1) 

    with rasterio.open(flowdir_tif_path, 'w', **profile) as dst:
        dst.write(data, 1)
print("integration complete!")
print("")


# ### 13 - 1/(W*S) (OK)


#13
# Process: Computing 1/(W*S) (Raster Calculator) (sa)
        
print("13 computing 1/(W*S)")
print("")
invCS_tif_path = os.path.join(endereco_processos, "invCS.tif").replace("\\", "/")

with rasterio.open(Weighting_Factor) as src1, rasterio.open(s_tif_path) as src2 : 
    
    profile = src1.profile 
    
    wfactor,wfactor_nodata = mascara(src1) 
    s, s_nodata= mascara(src2) 

    w_vezes_s = wfactor * s
    
    divisao_power = ma.power(w_vezes_s, -1)
    
with rasterio.open(invCS_tif_path, 'w', **profile) as dst:
    dst.write(divisao_power, 1)
    print(dst.nodata)
print(" complete!")
print("")




# ### 18 - Flowlenght - Distance_down_tif - taudem method

#this method substitues the flowlength step, that is a function from arcgis. 

distance_down_tif_path =  os.path.join(endereco_processos,"distance_down.tif").replace("\\", "/")
distance_down_tif = driver.Create(distance_down_tif_path,x_dim, y_dim, 1, gdal.GDT_Float64)
distance_down_tif= None

subprocess.run(["DinfDistDown","-ang", dtmfillokang_tif_path, "-fel",  Pits_Removed_DTM, "-src", target_tif_path,  
            "-wg", invCS_tif_path,"-dd", distance_down_tif_path,"-m", "min", "h" , "-nc"])




# ### 20 - DownslopeComponent - Raster Calculator (OK)

#20
print("20 Downslope component")

# Process: Computing Downslope Component (Raster Calculator) (sa)
Ddn_tif_path = os.path.join(endereco_processos,"Ddn.tif").replace("\\", "/")

with rasterio.open(distance_down_tif_path) as src1, rasterio.open(invCS_tif_path) as src2 : #invCS é o passo 13
    
    profile = src1.profile 
    
    x, x_nodata= mascara(src1)   
    inv, inv_nodata= mascara(src2)
    
    ddn = ma.where(x==0,inv,x)  #onde x for zero, ele coloca o valor de inv, outros casos, valor de x
    
    
with rasterio.open(Ddn_tif_path, 'w', **profile) as dst:
    dst.write(ddn, 1)
print("downslope component complete!")
print("")


IHC = os.path.join(endereco_saida, output_name)


# ### 21 - IHC

# Process: Computing Connectivity Index (Raster Calculator) (sa)
print("21 STARTING IHC")

with rasterio.open(Dup_tif_path) as src1, rasterio.open(Ddn_tif_path) as src2 : 
    profile = src1.profile 
    
    upslope, upslope_nodata = mascara(src1)
    downslope, downslope_nodata = mascara(src2)
   
    razao = ma.divide(upslope, downslope)

    ihc_final = ma.log10(razao)

    mask = downslope.mask

    ihc_final_mascara = ma.masked_array(ihc_final, mask = downslope.mask)
    
    
with rasterio.open(IHC, 'w', **profile) as dst:
    dst.write(ihc_final_mascara, 1)
    print(dst.nodata)
    
print("ihc complete!")
print("")

app.delete_process_folder()

print(input())
print("To close this window, press any key")
