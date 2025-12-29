program factorial;
var
  n, i, fact: integer;
begin
  read(n);
  fact := 1;
  i := 1;
  while i <= n do
  begin
    fact := fact * i;
    i := i + 1;
  end;
  write(fact);
end.
