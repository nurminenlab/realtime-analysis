t = tcpclient('localhost', 5100);
if t.NumBytesAvailable > 0
    output = read(t);
    disp(char(output))

end
clear t;