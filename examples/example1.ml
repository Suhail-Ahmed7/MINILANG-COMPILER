program example1;
var
  x, y: integer;
  max: integer;
begin
  read(x);
  read(y);
  if x > y then
    max := x  { no semicolon needed before else }
  else
    max := y; { semicolon needed if followed by another statement }
  write(max);
end.