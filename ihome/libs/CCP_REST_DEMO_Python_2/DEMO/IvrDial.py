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

  # IVR���
  # @param number   �����к��룬ΪDial�ڵ������
  # @param userdata �û����ݣ���<startservice>֪ͨ�з��أ�ֻ������д�����ַ���ΪDial�ڵ������
  # @param record   �Ƿ�¼����������Ϊtrue��false��Ĭ��ֵΪfalse��¼����ΪDial�ڵ������
def ivrDial(number,userdata,record):
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    #call createSubAccount
    result = rest.ivrDial(number,userdata,record)
    for k,v in result.iteritems(): 
        print '%s:%s' % (k, v)
   
   
#ivrDial('�����к���','�û�����',�Ƿ�¼��)