#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '�������ʺ�';

#���ʺ�Token
accountToken= '�������ʺ�Token';

#Ӧ��Id
appId='����Ӧ��ID';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

    # @param filename   ��ѡ����    �ļ���
    # @param path      ��ѡ����     �ļ�����·��

def MediaFileUpload(filename,path):

    
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    file_object = open(path,'rb')
    try:
        body = file_object.read()
    finally:
        file_object.close()
	
    result = rest.MediaFileUpload(filename,body)
    for k,v in result.iteritems(): 
            print '%s:%s' % (k, v)
   
   
#MediaFileUpload('�ļ���','�ļ�����·��')