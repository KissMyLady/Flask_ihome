#coding=gbk
#coding=utf-8

#-*- coding: UTF-8 -*-
from Cloudy_SMG import REST
import ConfigParser

#���ʺ�
accountSid= '�������ʺ�' 

#���ʺ�Token
accountToken= '�������ʺ�Token' 

#Ӧ��Id
appId='����Ӧ��ID' 

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com' 

#����˿� 
serverPort='8883' 

#REST�汾��
softVersion='2013-12-26' 

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id


def sendTemplateSMS(to, datas, tempId):
    #��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)
    
    result = rest.sendTemplateSMS(to, datas, tempId)
    
    for k, v in result.iteritems():
        
        if k == 'templateSMS':
            for k, s in v.iteritems():
                print('%s:%s' % (k, s))
        else:
            print('%s:%s' % (k, v))
    
   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)