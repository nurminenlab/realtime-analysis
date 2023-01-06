
t = tcpclient('localhost', 5100);
while t~=null
    output = read(t);
    data = char(output);
    fprintf(data)
end
clear t;