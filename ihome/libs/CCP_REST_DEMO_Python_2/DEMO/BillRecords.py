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

  # ��������
  # @param date     day ����ǰһ������ݣ���00:00 �C 23:59��
  # @param keywords   �ͻ��Ĳ�ѯ�������ɿͻ����ж��岢�ṩ����ͨѶƽ̨��Ĭ�ϲ�����Դ˲���

def billRecords(date,keywords):
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.billRecords(date,keywords)
    for k,v in result.iteritems(): 
        print '%s:%s' % (k, v)
   
   
#billRecords('��ѯ��ʽ','��ѯ����')