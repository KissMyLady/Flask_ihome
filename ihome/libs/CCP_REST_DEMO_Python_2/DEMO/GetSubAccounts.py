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

  # ��ȡ���ʺ�
  # @param startNo ��ʼ����ţ�Ĭ�ϴ�0��ʼ
  # @param offset һ�β�ѯ�������������С��1���������100��

def getSubAccounts(startNo,offset):

    
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    result = rest.getSubAccounts(startNo,offset)

    i=1
    for k,v in result.iteritems(): 
        
        if k=='SubAccount' :
            for m in v:
                print ('��'+str(i)+'�����ʺ�Ϊ')
                i=i+1
                for k,v in m.iteritems(): 
                    print '%s:%s' % (k, v)
        else:
            print '%s:%s' % (k, v)
   
#getSubAccounts('��ʼ�����','�������')