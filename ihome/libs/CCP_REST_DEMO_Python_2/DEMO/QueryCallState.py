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

    # ����״̬��ѯ
    # @param callSid   ��ѡ����    һ����32���ַ���ɵĵ绰Ψһ��ʶ��
    # @param action      ��ѡ����     ��ѯ���֪ͨ�Ļص�url��ַ 

def QueryCallState(callid,action):

    
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.QueryCallState(callid,action)
    for k,v in result.iteritems(): 
            print '%s:%s' % (k, v)
   
   
#QueryCallState('callSid','��ѯ���֪ͨ�Ļص�url��ַ')