i=0;
t = tcpclient('localhost', 51001);

while i < 3
    if t.NumBytesAvailable > 0
        output = read(t);
        data = char(output(1:4));
        pwrcmd = str2double(data)
        i = i+1;
    end
end

clear t;