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

# ����ģ���ѯ
# @param templateId  ��ѡ����   ģ��Id�������˲�����ѯȫ������ģ�� 
def QuerySMSTemplate(templateId):
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.QuerySMSTemplate(templateId)
    i=1
    for k,v in result.iteritems(): 
        
        if k=='TemplateSMS' :
            for m in v:
                print ('��'+str(i)+'��ģ��')
                i=i+1
                for k,v in m.iteritems(): 
                    print '%s:%s' % (k, v)
        else:
            print '%s:%s' % (k, v)
   
   
#QuerySMSTemplate('')