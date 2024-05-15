from django import forms
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from .models import *
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail



class Form_supervisor(forms.Form):
    nom = forms.CharField(required=True, max_length=supervisor._meta.get_field(
        'nom').max_length, widget=forms.TextInput(attrs={'id': "nom", 'name': "nom", 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;", 'placeholder': 'Last Name'}))
    
    prenom = forms.CharField(required=True, max_length=supervisor._meta.get_field(
        'prenom').max_length, widget=forms.TextInput(attrs={'id': 'prenom', 'name': 'prenom', 'placeholder': 'First Name', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))
    
    telephone = forms.CharField(required=True, max_length=supervisor._meta.get_field(
        'NB_GSM').max_length, widget=forms.TextInput(attrs={'id': 'NB_GSM', 'name': 'NB_GSM', 'placeholder': 'Phone', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))
    
    pseudo = forms.CharField(required=True, max_length=supervisor._meta.get_field(
        'pseudo').max_length, widget=forms.TextInput(attrs={'id': 'pseudo', 'name': 'pseudo', 'placeholder': 'Pseudo', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))
    
    email = forms.EmailField(max_length=supervisor._meta.get_field(
        'e_mail').max_length, required=True, widget=forms.EmailInput(attrs={'id': 'email', 'name': 'email', 'placeholder': 'Mail', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))
    
    mot_de_passe = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'id': 'password', 'name': 'password', 'placeholder': 'Password', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))
    
    confirmation_mot_de_passe = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'id': 'password1', 'name': 'password1', 'placeholder': 'Re-enter password', 'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"}))


    def is_valid(self):
        self.validate_nom()
        self.validate_prenom()
        self.validate_pseudo()
        self.validate_email()
        self.validate_telephone()
        self.validate_mot_de_passe()
        self.validate_confirmation_mot_de_passe()
        value = super(Form_supervisor, self).is_valid()
        return value

    def validate_nom(self):
        nom = self.data['nom']
        if any(char.isdigit() for char in nom):
            self.add_error("nom", "Nom est incorrect!")

    def validate_prenom(self):
        prenom = self.data['prenom']
        if any(char.isdigit() for char in prenom):
            self.add_error("prenom", "Prenom est incorrect!")

    def validate_pseudo(self):
        pseudo = self.data['pseudo']
        if supervisor.objects.filter(pseudo=pseudo).exists():
            self.add_error("pseudo", "pseudo déja existant!")

    def validate_email(self):
        email = self.data['email']
        if supervisor.objects.filter(e_mail=email).exists():
            self.add_error("email", "email déja existant!")

    def validate_telephone(self):
        telephone = self.data['telephone']
        if not telephone.isdigit():
            self.add_error("telephone", "Téléphone est incorrect!")

    def validate_mot_de_passe(self):
        mot_de_passe = self.data['mot_de_passe']
        if len(mot_de_passe) < 8:
            self.add_error("mot_de_passe", "Le mot de passe doit contenir au moins 8 caractères.")

    def validate_confirmation_mot_de_passe(self):
        confirmation_mot_de_passe = self.data['confirmation_mot_de_passe']
        mot_de_passe = self.data['mot_de_passe']
        if confirmation_mot_de_passe != mot_de_passe:
            self.add_error("confirmation_mot_de_passe", "Les mots de passe ne correspondent pas.")

    def enregistrer(self):
            nom = self.cleaned_data['nom']
            prenom = self.cleaned_data['prenom']
            email = self.cleaned_data['email']
            pseudo = self.cleaned_data['pseudo']
            telephone = self.cleaned_data['telephone']
            confirmation_mot_de_passe = self.cleaned_data['confirmation_mot_de_passe']
            data = supervisor(nom=nom, prenom=prenom, pseudo=pseudo,NB_GSM=telephone, e_mail=email)
            data.save()
            
            data = User.objects.create_user(pseudo, email, confirmation_mot_de_passe)
            data.save()

class Form_client(forms.Form):
    
    nom = forms.CharField(required=True, max_length=client._meta.get_field(
        'nom').max_length, widget=forms.TextInput(attrs={'id': "nom", 'name': "nom", 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color:#e6e5e5;", 'placeholder': 'Last Name'}))
    
    prenom = forms.CharField(required=True, max_length=client._meta.get_field(
        'prenom').max_length, widget=forms.TextInput(attrs={'id': 'prenom', 'name': 'prenom', 'placeholder': 'First Name', 'class': "form-control  p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))
    
    telephone = forms.CharField(required=True, max_length=client._meta.get_field(
        'NB_GSM').max_length, widget=forms.TextInput(attrs={'id': 'NB_GSM', 'name': 'NB_GSM', 'placeholder': 'Phone', 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))
    
    pseudo = forms.CharField(required=True, max_length=client._meta.get_field(
        'pseudo').max_length, widget=forms.TextInput(attrs={'id': 'pseudo', 'name': 'pseudo', 'placeholder': 'Pseudo', 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))
    
    email = forms.EmailField(max_length=client._meta.get_field(
        'e_mail').max_length, required=True, widget=forms.EmailInput(attrs={'id': 'email', 'name': 'email', 'placeholder': 'Mail', 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))
    
    mot_de_passe = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'id': 'password', 'name': 'password', 'placeholder': 'Password', 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))
    
    confirmation_mot_de_passe = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'id': 'password1', 'name': 'password1', 'placeholder': 'Re-enter password', 'class': "form-control p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;"}))

    image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'id': "image", 'name': "image", 'class': "form-control-file", 'style': "font-size: 15px;"}))
    

    def is_valid(self):
            nom = self.data['nom']
            if any(char.isdigit() for char in nom):
                self.add_error("nom", "Nom est incorrect!")
            prenom = self.data['prenom']
            if any(char.isdigit() for char in prenom):
                self.add_error("prenom", "Prenom est incorrect!")
            pseudo = self.data['pseudo']
            if client.objects.filter(pseudo=pseudo).exists():
                self.add_error("pseudo", "pseudo déja existant!")
            email = self.data['email']
            if client.objects.filter(e_mail=email).exists():
                self.add_error("email", "email déja existant!")
            telephone = self.data['telephone']
            if not telephone.isdigit():
                self.add_error("telephone", "Téléphone est incorrect!")
            mot_de_passe = self.data['mot_de_passe']
            if len(mot_de_passe) < 8:
                self.add_error(
                    "mot_de_passe", "Le mot de passe doit contenir au moins 8 caractères.")
            confirmation_mot_de_passe = self.data['confirmation_mot_de_passe']
            if confirmation_mot_de_passe != mot_de_passe:
                self.add_error("confirmation_mot_de_passe",
                            "Les mots de passe ne correspondent pas.")
            value = super(Form_client, self).is_valid()
            return value


    def enregistrer(self,idd,pseud):

            
            nom = self.cleaned_data['nom']
            prenom = self.cleaned_data['prenom']
            email = self.cleaned_data['email']
            pseudo = self.cleaned_data['pseudo']
            img = self.cleaned_data['image']
            telephone = self.cleaned_data['telephone']
            confirmation_mot_de_passe = self.cleaned_data['confirmation_mot_de_passe']
            superviseur = supervisor.objects.get(pseudo=pseud)
            
            new_client = client(nom=nom, prenom=prenom, pseudo=pseudo,image=img,
                            NB_GSM=telephone, e_mail=email,supervisor=superviseur)
            
            new_client.save()
            
            my_project = myProject.objects.get(polygon_id=idd) 
            my_project.clientp = new_client
            my_project.save()           
            
            data = User.objects.create_user(
                pseudo, email, confirmation_mot_de_passe)
            data.save()
            
            self.new_client = new_client 

            # data2 =Project(nomp=nomp,desc=desc,debut=debut,fin=fin,city=city,location=location)
            # data2.save()
            # Prepare the email subject and message
            print('reaaadyyyy')
            subject = 'Client data!'
            context = {
                'client_name': nom,  # Replace with the appropriate client name
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'phone': telephone,
                'mdp': confirmation_mot_de_passe,
                'superviseur' : superviseur,  # Replace with the appropriate client data
            }
            html_message = render_to_string('email_template.html', context)
            plain_message = strip_tags(html_message)
            
            
           
            # Send the email
            #send_mail(subject, plain_message, 'hm2845187@gmail.com', [email], html_message=html_message)
            #print('doooooooooooone')

class Form_project(forms.Form):

    nomp = forms.CharField(required=True,max_length=myProject._meta.get_field(
        'nomp').max_length, widget=forms.TextInput(attrs={'id': "nomp", 'name': "nomp", 'class': "form-control  p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;", 'placeholder': 'Project Name'}))
    descp = forms.CharField( required=False, max_length=myProject._meta.get_field(
        'descp').max_length, widget=forms.Textarea(attrs={'id': "descp", 'name': "descp", 'class': "form-control  p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5; height:70px; width:600px; ", 'placeholder': 'Write description about the project'}))
    
    cityp = forms.CharField(required=True, max_length=myProject._meta.get_field(
        'cityp').max_length, widget=forms.TextInput(attrs={'id': "cityp", 'name': "cityp", 'class': "form-control  p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5;", 'placeholder': 'Region Name'}))
 
    clientp = forms.ModelChoiceField(queryset=client.objects.all(),required=False,empty_label='None', widget=forms.Select(attrs={'id': "clientp", 'name': "clientp", 'class': "form-control  p-8 mb-4 rounded", 'style': "font-size: 15px; background-color: #e6e5e5; width:170px;", 'placeholder': 'Select Client'}))
    
    piece_joinde = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'id': "piece_joinde", 'name': "piece_joinde", 'class': "form-control-file", 'style': "font-size: 15px;"}))
    
    def is_valid(self):
            nomp = self.data['nomp']
            if any(char.isdigit() for char in nomp):
                self.add_error("nomp", "Nom projet est incorrect!")

            

            cityp = self.data['cityp']
            if any(char.isdigit() for char in cityp):
                self.add_error("city", "city est incorrect!")

            value = super(Form_project, self).is_valid()
            return value

    def enregistrerProj(self):
        nomp = self.cleaned_data['nomp']
        descp = self.cleaned_data['descp']
        # debutp = self.cleaned_data['debutp']
        # finp = self.cleaned_data['finp']
        cityp = self.cleaned_data['cityp']
        clientp = self.cleaned_data['clientp']

class LoginForm(forms.Form):
    pseudo = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'pseudo',
                'name': 'pseudo',
                'placeholder': 'Pseudo',
                'class': "form-control shadow-lg p-6 mb-6 rounded",
                'style': "font-size: 20px; background-color: #DFD9DB;"
            }
        )
    )
    mot_de_passe = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'name': 'password',
                'placeholder': 'Mot de passe',
                'class': "form-control shadow-lg p-6 mb-6 rounded",
                'style': "font-size: 20px; background-color: #DFD9DB;"
            }
        )
    )




    def is_valid(self, request):
        pseudo = self.data['pseudo']
        mot_de_passe = self.data['mot_de_passe']
        if User.objects.filter(username=pseudo).exists():
            # Here, we assign the result of authenticate() to a variable
            user = authenticate(request, username=pseudo,
                                password=mot_de_passe)
            if user is None:
                self.add_error(
                    "mot_de_passe", "Les mots de passe ne correspondent pas.")
        else:
            self.add_error("pseudo", "Ce compte n'existe pas.")
        return super(LoginForm, self).is_valid()
