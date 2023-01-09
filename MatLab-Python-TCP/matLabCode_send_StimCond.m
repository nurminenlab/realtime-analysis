t = tcpclient('localhost', 51005);

if t.NumBytesAvailable > 0
    output = read(t);
    message = char(output);
    fprintf(message);
end
write(t,'a')
write(t,'b')
write(t,'c')

clear t;