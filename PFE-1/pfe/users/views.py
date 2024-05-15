from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from users.models import client
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
import json  # Add this line to import the json module


# Create your views here.

def connectas(request):
    return render(request, 'connectas.html')

def connectasclient(request):
    if request.method == 'POST':
        formulaire = LoginForm(request.POST)
        if formulaire.is_valid(request):
            pseudo = formulaire.cleaned_data['pseudo']
            mot_de_passe = formulaire.cleaned_data['mot_de_passe']
            data = authenticate(request, username=pseudo,
                                password=mot_de_passe)
            if data is not None:
                login(request, data)

                clientp = client.objects.get(pseudo=pseudo)
                # project = myProject.objects.get(clientp=clientp)
                
            return redirect('client_project',pseudo)
        # We pass the form to the template even if it is not valid
        return render(request, 'login_as_client.html', {'form': formulaire})
    # We pass the form to the template for GET requests
    return render(request, 'login_as_client.html', {'form': LoginForm()})

def connectassupervisor(request):
    if request.method == 'POST':
        formulaire = LoginForm(request.POST)
        if formulaire.is_valid(request):
            pseudo = formulaire.cleaned_data['pseudo']
            mot_de_passe = formulaire.cleaned_data['mot_de_passe']
            data = authenticate(request, username=pseudo,password=mot_de_passe)
            if data is not None:
                login(request, data)
                #### on va redirect dashboard #####
                # return redirect('map/')
            return redirect('display',pseudo)
        # We pass the form to the template even if it is not valid
        return render(request, 'login.html', {'form': formulaire})
    # We pass the form to the template for GET requests
    return render(request, 'login.html', {'form': LoginForm()})

def compte(request, pk, variable=None, pseudo=None):
    if pk == 'supervisor':
        if request.method == 'POST':
            formulaire = Form_supervisor(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'supervisor'
                #######PB here
                return redirect('add_client',pseudo)
                # return redirect('map', variable, pseudo)
            return render(request, 'signup.html', {'form': formulaire})
        return render(request, 'signup.html', {'form': Form_supervisor()})
    else:
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'client'
                ####### redirect dashboard normally
                #return redirect('map/',variable, pseudo)
                return redirect('interface_c')
            return render(request, 'signup.html', {'form': formulaire})
        return render(request, 'signup.html', {'form': Form_client()})
       

def add_project(request,pseudo):
    supervisors = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisors).order_by('-polygon_id')

    clients = client.objects.all()
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        nomp = request.POST.get('nomp')
        descp = request.POST.get('descp')
        debutp = request.POST.get('debutp')
        finp = request.POST.get('finp')
        cityp = request.POST.get('cityp')
        piece_joinde =request.POST.get('piece_joinde')

        
        if formulairep.is_valid():

            selected_client_id = request.POST.get('clientp')
                  
            formulairep.enregistrerProj()

            if selected_client_id:
                selected_client = client.objects.get(id=selected_client_id)

                instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,clientp=selected_client,supervisorp=supervisors,piece_joinde=piece_joinde)
                instance.save()
                return redirect('add_polygones',pseudo=pseudo,id=instance.polygon_id)
            else:
                instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,supervisorp=supervisors,piece_joinde=piece_joinde)
                instance.save()                
                return redirect('add_client',pseud=pseudo,idd=instance.polygon_id)
            
            
        return render(request, 'addproj.html', {'form': formulairep,'projects':projects,'supervisor':supervisors})
    return render(request, 'addproj.html', {'form': Form_project(),'projects':projects,'supervisor':supervisors})

def add_polygones(request,pseudo,id):
    superviseur = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=superviseur).order_by('-polygon_id')
        
    project = myProject.objects.get(polygon_id=id)   
    if request.method == 'POST':

        multiPolygone= request.POST.get('points')
        multiPolygone_dict = json.loads(multiPolygone)
        multipolygon = GEOSGeometry(multiPolygone, srid=4326)

        project.geomp = multipolygon
        project.save()         
        
        polygons = []

        for polygon_coords in multiPolygone_dict['coordinates']:
            print('-----------')
            for i in range(len(polygon_coords)): 
                poly_str = 'POLYGON(({0}))'.format(','.join([' '.join(map(str, c)) for c in polygon_coords[i]]))
                print('poly_str',poly_str)
                polygon = GEOSGeometry(poly_str, srid=4326)
                parcelle_obj = parcelle(poly=polygon,project=project)
                    # parcelle_obj.project = instance  # set the project attribute of the parcelle
                parcelle_obj.save()
                polygons.append(polygon)       
                    
            # return redirect('add_client',id=instance.polygon_id)
        return redirect('addcage',pseudo=pseudo,id=project.polygon_id)
        
    return render(request, 'addpolyg.html', {'projects':projects,'supervisor':superviseur,'project':project})

def add_client(request,idd,pseud):
        # project = myProject.objects.get(polygon_id=id)
        superviseur = supervisor.objects.get(pseudo=pseud)
        projects = myProject.objects.filter(supervisorp=superviseur).order_by('-polygon_id')
        print('----------',projects)
        project = myProject.objects.get(polygon_id=idd) 
        print('----------',project.polygon_id)

        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            image = request.FILES.get('profile')

            
          
            if formulaire.is_valid():
                
                formulaire.enregistrer(idd,pseud)
                new_client = formulaire.new_client
                print(new_client)

                new_client.image=image
                new_client.save()
                
                

 
                return redirect('add_polygones',pseudo=pseud,id=project.polygon_id)
            return render(request, 'addclient.html', {'form': formulaire,'supervisor':superviseur,'projects':projects,'project':project})
        return render(request, 'addclient.html', {'form': Form_client(),'supervisor':superviseur,'projects':projects,'project':project})

def display(request,pseudo):
    # projects = myProject.objects.all()
    # supervisors = supervisor.objects.get(pseudo=pseudo)
    
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    print("/////////", supervisor_obj.pseudo)
    print("/////projects////",projects )

    for proj in projects :
        print("/////proj////", proj)
        
    if request.method == 'POST':
    #     return redirect('project_1',pseudo)
        return redirect('add_project', pseudo=pseudo)

    return render(request, 'display.html', {'projects':projects,'supervisor_obj':supervisor_obj})

def display_polygone(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    print("//supervisor_obj/", supervisor_obj)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)
    print("//project/", project.supervisorp)

    if request.method == 'POST':
        # id=instance.polygon_id

       
        return redirect('addcage',pseudo,id)
    return render(request, 'displaypoly.html', {'projects':projects,'project':project,'supervisor':supervisor_obj})

def addcage(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)

    marker = cage.objects.all()
    cageq = cage.objects.filter(polyg=project)

    if request.method == 'POST':
        cage_name = request.POST.get('nom')  
        range_str = request.POST.get('range')
        cage_range = int(range_str) 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        diametre=request.POST.get('diameter')
        point=Point(x=float(mylongitude),y=float(mylatitude))
        description=request.POST.get('description')
        project_id = request.POST.get('polyg')
        namep = request.POST.get('parcelle')

        project_instance = myProject.objects.get(polygon_id=project_id)
        parcelles = parcelle.objects.filter(project=project_instance)
        list_p=[]
        for p in parcelles:
            list_p.append(p)
        print('----------------------',list_p)
        
        instance = cage(nom=cage_name, centre=point, latitude_centre=mylatitude, longitude_centre=mylongitude, cage_range=cage_range, diametre=diametre, description=description, polyg=project_instance, parc=list_p[cage_range-1],)        
        instance.save()

        return redirect('addnode',pseudo,id)

    return render(request, 'add_cage.html', { 'projects': projects, 'project': project,'nodee':cageq,'supervisor':supervisor_obj})
    
def add_node(request, id, pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)
    cages = cage.objects.filter(polyg=project)
    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
 
    if request.method == 'POST':
        node_name = request.POST.get('nom')
        Sensors = request.POST.get('Sensors') 
        reference = request.POST.get('reference') 
        range_str = request.POST.get('range')
        node_range = int(range_str) 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        cage_id = request.POST.get('cage')  # Récupérer l'ID de la cage sélectionnée
        point = Point(x=float(mylongitude), y=float(mylatitude))
        project_id = request.POST.get('polyg')
        namep = request.POST.get('parcelle')
       
        project_instance = myProject.objects.get(polygon_id=project_id)
        parcelles = parcelle.objects.filter(project=project_instance)
        list_p = []
        for p in parcelles:
            list_p.append(p)
        
        # Récupérer l'instance de la cage sélectionnée
        selected_cage = cage.objects.get(Idcage=cage_id)
        
        # Créer une instance de nœud en associant à la fois le projet et la cage sélectionnée
        instance = node(position=point, nom=node_name, polyg=project_instance, parc=list_p[node_range-1],
                        latitude=mylatitude, longitude=mylongitude, reference=reference, node_range=node_range,
                        Sensors=Sensors, cage=selected_cage)  # Associer le nœud à la cage sélectionnée
        instance.save()
        
        # Créer une nouvelle instance de données pour ce nœud
        new_data = Data(distance=0, node=instance)
        new_data.save()

        datas = Data.objects.filter(node=instance)

        return redirect('all', pseudo, id)

    return render(request, 'add_node.html', {'projects': projects, 'project': project, 'nodee': nodeq,
                                              'supervisor': supervisor_obj, 'cages': cages})

def all_node(request, iid, pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    my_project = myProject.objects.get(polygon_id=iid) 
    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
    cages = cage.objects.filter(polyg=my_project)

    nod = node.objects.filter(polyg=my_project).order_by('-Idnode').first()
    ldat = Data.objects.filter(node=nod).order_by('-IdData').first()
     
    data_list = []
    for n in nodes:
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(ds)

    lastd = data_list[0]
    
    context = {
        'projects': projects,
        'project': my_project,
        'nodee': nodes,
        'cages': cages,
        'lastd': lastd,
        'ldn': data_list,
        'ldat': ldat,
        'supervisor': supervisor_obj
    }
    return render(request, 'all.html', context)

def update_distance(request, id):
    # get updated weather information
    my_project = myProject.objects.get(polygon_id=id)

    # lasst node added
    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')

    ldata =[]
    for n in nodes:
        dat= Data.objects.filter(node=n).order_by('-IdData').first()
        ldata.append( {
            
        'distance': dat.distance,
        'RSSI' : n.RSSI,
        'battery' :n.Battery_value,
        'reference' :n.reference,
        'node_range' : n.node_range,
        'node':n.nom,
        'x':n.position.x,
        'y':n.position.y,
        }
            
        )
        

    onode = nodes[0]
    
    datas = Data.objects.filter(node=onode).order_by('-IdData')
    # last data coming
    datao = datas.first()
   # print('----datao',datao)
    node_rssi = onode.RSSI
    node_battery=onode.Battery_value
    node_name =onode.nom
    node_reference =onode.reference
    node_range=onode.node_range
    dataa = {
        'distance': datao.distance,
        'RSSI' : node_rssi,
        'battery' :node_battery,
        'reference' :node_reference,
        'node_range' : node_range,
        'node':node_name,
        'x':onode.position.x,
        'y':onode.position.y,
        }
    # return a JsonResponse with the updated data
    return JsonResponse(dataa, safe=False)

def ALL(request, id, pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    onode = nodes[0]  # Node_instance // onlyy for the last one

    datas = Data.objects.filter(node=onode).order_by('-IdData')
    data = datas.first()

    nodeq = node.objects.filter(polyg=project)
    nodes_data = []
    for node_instance in nodes:
        datas = Data.objects.filter(node=node_instance).order_by('-IdData')
        data = datas.first()
        nodes_data.append({'node_instance': node_instance, 'data': data})

    data_list = []
    for n in nodes:
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(ds)

    cages = []  # Obtenez la liste des cages de votre modèle de données
    # Exemple : cages = Cage.objects.filter(project=project)

    context = {
        'nodes_data': nodes_data,
        'supervisor': supervisor_obj,
        'nodee': nodeq,
        'node': onode,
        'projects': projects,
        'project': project,
        'parm': data,
        'ldn': data_list,
        'cages': cages,
    }

    return render(request, 'ALL_node.html', context)

def final(request, id, pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    nodeq = node.objects.filter(polyg=project)
    cages = cage.objects.filter(polyg=project)  # Récupérer les cages associées au projet
    
    data_list = []
    for n in nodes:
        dat = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(dat)

    context = {
        'supervisor': supervisor_obj,
        'projects': projects,
        'project': project,
        'nodes': nodes,
        'nodee': nodeq,
        'ldn': data_list,
        'cages': cages  # Ajoutez les cages au contexte
    }

    return render(request, 'final.html', context)

def final2(request, id, pseudo, idnode):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    nod = node.objects.get(Idnode=idnode) 
    ds = Data.objects.filter(node=nod).order_by('-IdData').first()
    nodeq = node.objects.filter(polyg=project)
    
    data_list = []
    for n in nodes:
        dat = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(dat)

    lDist =[]
    dss = Data.objects.filter(node=nod).order_by('-IdData')
    for d in dss:
        lDist.append(d.distance)

    cages = cage.objects.filter(polyg=project)  # Récupérer les cages associées au projet
    
    context = {
        'supervisor': supervisor_obj,
        'projects': projects,
        'project': project,
        'nodes': nodes,
        'nod': nod,
        'ds': ds,
        'lDist': lDist,
        'ldn': data_list,
        'nodee': nodeq,
        'cages': cages  # Ajoutez les cages au contexte
    }
    return render(request, 'final2.html', context)

def final3(request, id, pseudo, idnode):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj).order_by('-polygon_id')
    
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    nod = node.objects.get(Idnode=idnode) 
    ds = Data.objects.filter(node=nod).order_by('-IdData').first()
    
    nodeq = node.objects.filter(polyg=project)
    
    data_list = []
    for n in nodes:
        dat = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(dat)
        
    # Récupérer les cages associées au projet
    cages = cage.objects.filter(polyg=project)
    
    context = {
        'supervisor': supervisor_obj,
        'projects': projects,
        'project': project,
        'nodes': nodes,
        'nod': nod,
        'ds': ds,
        'ldn': data_list,
        'nodee': nodeq,
        'cages': cages,
    }
    
    return render(request, 'final3.html', context)

def delete_project(request,pseudo,id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    
    project = myProject.objects.get(polygon_id=id)
    
    project.delete()
    return redirect('display',pseudo=supervisor_obj.pseudo)

def modify_1(request, pseudo, id):

    supervisors = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisors).order_by('-polygon_id')
    project = myProject.objects.get(polygon_id=id)

    
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        new_name = request.POST.get('nomp')
        new_descp = request.POST.get('descp')
        new_debutp = request.POST.get('debutp')
        new_finp = request.POST.get('finp')
        new_cityp = request.POST.get('cityp')
        new_piece_joinde =request.POST.get('piece_joinde')


        if formulairep.is_valid():
            # Get the selected client from the form
            selected_client_id = request.POST.get('clientp')               
            formulairep.enregistrerProj()

            if selected_client_id:
                new_client = client.objects.get(id=selected_client_id)
                project.nomp=new_name
                project.descp=new_descp
                project.debutp=new_debutp
                project.finp=new_finp
                project.cityp=new_cityp
                project.clientp=new_client
                project.piece_joinde=new_piece_joinde
                project.save()
                return redirect('ALL_node',pseudo=pseudo,id=project.polygon_id)
            else:
                project.nomp=new_name
                project.descp=new_descp
                project.debutp=new_debutp
                project.finp=new_finp
                project.cityp=new_cityp
                project.piece_joinde=new_piece_joinde
                project.save()              
                return redirect('ALL_node',pseudo=pseudo,id=project.polygon_id)

            
        return render(request, 'modify_1.html', {'form': formulairep,'projects':projects,'supervisor':supervisors})
    return render(request, 'modify_1.html', {'form': Form_project(),'projects':projects,'supervisor':supervisors})

def modify_2(request, pseudo, id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project)
    
    for n in nodes:
        n.delete()
    
    project.geomp = ""
    project.save()

    return redirect('add_polygones', pseudo=supervisor_obj.pseudo,id=project.polygon_id)

def modify_3(request, pseudo, id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project)
    
    if request.method == 'POST':
        node_to_delete_name = request.POST.get('node_to_delete')
        node_to_delete = node.objects.get(nom=node_to_delete_name)
        node_to_delete.delete()
        return redirect('addnode', pseudo=supervisor_obj.pseudo, id=project.polygon_id)
        
#def start_mqtt(request,id):
    # Start the MQTT client
    # start_mqtt_client(id)
    # mqtt.client.loop_forever()
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    #return render(request, 'all.html', {})

