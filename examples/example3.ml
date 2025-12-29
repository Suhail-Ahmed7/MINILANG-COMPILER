program calculator;
var
  a, b: integer;
  result: integer;
  flag: boolean;
begin
  read(a);
  read(b);
  flag := a > b;
  
  if flag then
    result := a * b
  else
    result := a + b;
  
  write(result);
end.