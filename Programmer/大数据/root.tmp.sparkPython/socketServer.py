import socket
server = socket.socket() #创建socket对象
server.bind(('localhost',9999)) #绑定ip和端口
server.listen(1) #监听端口
while 1:
    print('waiting conn...')
    conn,addr = server.accept()#阻塞等待客户端发送
    print('conn is success %s' % addr[0])
    print('send')
    conn.send('had,had,i,i,love'.encode())
    conn.close()
    print('conn is close')