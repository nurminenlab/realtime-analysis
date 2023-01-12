t = tcpclient('localhost', 51005);

if t.NumBytesAvailable > 0
    output = read(t);
    message = char(output);
    fprintf(message);
end
n = strlength('d');
write(t,n);
write(t,'d');
write(t,strlength('c'));
write(t,'c');
write(t,strlength('a'));
write(t,'a');
write(t,strlength('b'));
write(t,'b');
write(t,strlength('e'));
write(t,'e');

write(t,strlength('end'));
write(t,'end');

write(t,strlength('d'));
write(t,'d');
write(t,strlength('c'));
write(t,'c');
write(t,strlength('a'));
write(t,'a');
write(t,strlength('b'));
write(t,'b');
write(t,strlength('e'));
write(t,'e');

write(t,strlength('d'));
write(t,'d');
write(t,strlength('c'));
write(t,'c');
write(t,strlength('a'));
write(t,'a');
write(t,strlength('b'));
write(t,'b');
write(t,strlength('e'));
write(t,'e');

write(t,strlength('d'));
write(t,'d');
write(t,strlength('c'));
write(t,'c');
write(t,strlength('a'));
write(t,'a');
write(t,strlength('b'));
write(t,'b');
write(t,strlength('e'));
write(t,'e');

write(t,strlength('d'));
write(t,'d');
write(t,strlength('c'));
write(t,'c');
write(t,strlength('a'));
write(t,'a');
write(t,strlength('b'));
write(t,'b');
write(t,strlength('e'));
write(t,'e');
clear t;