from tkinter import *
import re
import psutil
import socket
from pyftpdlib import servers
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from tkinter.filedialog import askdirectory
from threading import Thread

server=None
class net:

    def getInter(self):
        self.net_ip = psutil.net_if_addrs()
        self.ip_addr=[]
        for ip in self.net_ip:
            if self.net_ip[ip][0].broadcast != None and self.net_ip[ip][0].netmask!=None:
                self.ip_addr.append(ip)
        return tuple(self.ip_addr)

    def getIPaddr(self,Inter):
        return self.net_ip[Inter][0].address

class front:


    def __init__(self,win):
        self.window=win
        self.window.wm_minsize(width=500, height=450)
        #self.window.wm_maxsize(width=650, height=450)
        self.set_front()

    def __del_(self):
        exit(0)

    def set_front(self):
        self.net_obj=net()
        self.net_det=self.net_obj.getInter()

        self.ip_var=StringVar(master=self.window)
        self.ip_var.set(self.net_det[0])
        self.ip_var.trace_add('write', self.set_lab)

        self.inter_opt=OptionMenu(self.window,self.ip_var,*self.net_det)
        self.inter_opt.grid(row=1,column=2)

        self.port_spin=Spinbox(master=self.window, from_=1024 ,to=2058)
        self.port_spin.grid(row=1,column=6)

        self.username_text=Text(master=self.window,width=10,height=1)
        self.username_text.grid(row=3,column=4,ipadx=10)
        self.username_text.insert("1.0", "admin")

        self.userpass_text=Text(master=self.window,width=10,height=1)
        self.userpass_text.grid(row=4,column=4,ipadx=10)
        self.userpass_text.insert("1.0", "admin")

        self.dir_text=Text(master=self.window, height=1,width=30)
        self.dir_text.bind('<Button-1>',self.set_dir)
        self.dir_text.grid(row=3,column=5,ipadx=10,columnspan=2)

        self.set_label()
        self.set_radio()
        self.set_button()
        self.set_checkbox()

    def set_checkbox(self):
        self.checkbox_var=IntVar()
        self.read_check=Checkbutton(master=self.window,text="ReadDir",onvalue=1,offvalue=0)
        self.read_check.grid(row=4,column=5)
        self.write_check=Checkbutton(master=self.window,text="WriteDir",onvalue=1,offvalue=0)
        self.write_check.grid(row=4,column=6)

    def set_button(self):

        self.connect_button=Button(master=self.window,text='Create FTP')
        self.connect_button.bind(sequence='<Button-1>', func=self.thread_cre)
        self.connect_button.grid(row=5,column=3,ipadx=10,padx=10,pady=10)

    def FTPCreation(self):
        button_text=self.connect_button.cget('text')
        default='Create FTP'
        ipvar=self.get_ipaddr()
        portval=self.port_spin.get()
        dirval=self.dir_text.get(index1='1.0', index2=None)
        if button_text==default:
            self.connect_button.clipboard_clear()
            self.connect_button.config(text='Disable FTP')
            self.create(ip=ipvar,port=portval,user_dir=dirval,permission=0)
        else:
            self.connect_button.config(text=default)
            self.destroy()

    def create(self,ip,port,user_dir,user_name=None,user_pass=None,permission=0,user=0):
        self.handler= FTPHandler
        global server
        auth =DummyAuthorizer()
        address=(ip,port)
        perms="elrafmwd"
        #if(permission>=0):
        #   perms="elr"
        #if(permission>=1):
        #    perms=prems.append("afmw")
        #if(permission==2):
        #    perms=prems.append("d")
        if(user==1):
            auth.add_user(user_name, user_pass,user_dir, perm=perms)
        else:
            auth.add_anonymous(user_dir, perm=perms)

        self.handler.authorizer=auth
        if server==None:
            server=servers.FTPServer(address,self.handler)
        server.serve_forever()

    def destroy(self):
        global server
        #self.handler.close()
        server.close_all()
        server=None

    def thread_cre(self,event):
        Thread(target=self.FTPCreation).start()

    def set_radio(self):

        self.radio_var=IntVar()
        self.anonyms_rb=Radiobutton(master=self.window,text="Anonymous",variable=self.radio_var,value=0)
        self.anonyms_rb.select()
        self.anonyms_rb.grid(row=3,column=1)
        self.user_rb=Radiobutton(master=self.window,text="Valid Users",variable=self.radio_var,value=1)
        self.user_rb.grid(row=4,column=1)

    def set_dir(self,event):
        dir_val=askdirectory(master=self.window,title="Choose FTP Directory")
        self.dir_text.delete("1.0")
        self.dir_text.insert("1.0",dir_val)

    def set_lab(self,*args):
        self.set_label()


    def set_label(self):
        self.ch_label=Label(self.window,text="Choose Interface:")
        self.ch_label.grid(row=1,column=1,padx=10,pady=10)
        self.ip_label=Label(self.window,text="IP Address:")
        self.ip_label.grid(row=1,column=3,padx=10,pady=10)
        ip=self.get_ipaddr()
        self.ip_addr=Label(master=self.window,text=ip)
        self.ip_addr.grid(row=1,column=4,pady=10)
        self.port_label=Label(master=self.window,text='Port:')
        self.port_label.grid(row=1,column=5,padx=20,pady=10)


        self.user_label=Label(master=self.window, text="Choose User:")
        self.user_label.grid(row=2,column=1,padx=10,pady=10)
        self.userdet_label=Label(master=self.window,text="User Detail:")
        self.userdet_label.grid(row=2,column=4,padx=10,pady=10)

        self.username_label=Label(master=self.window, text="User Name :")
        self.username_label.grid(row=3,column=3)

        self.userpass_label=Label(master=self.window, text="User Pass :")
        self.userpass_label.grid(row=4,column=3)

    def get_ipaddr(self):
        return self.net_obj.getIPaddr(Inter=self.ip_var.get())

window=Tk(className='FTP')
front(window)
window.mainloop()
