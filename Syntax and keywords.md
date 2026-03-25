# RawLang Syntax and Keywords

## Header

```rawlang
language should be python
```

Supported targets:
- python
- javascript
- golang
- rust

## Core statements

### Variables
```rawlang
make x = 10
assign 42 to x
```

### Collections
```rawlang
make list nums = 1 2 3
make set tags = "a" "b"
make tuple pair = 1 2
make object user = name "Raw" age 19
```

### Print
```rawlang
print "hello"
prints x
```

### Function
```rawlang
create function add with parameters x, y which
return x + y
.
```

### Call
```rawlang
call add with arguments 10, 20
```

### Condition
```rawlang
check if x > 10
print "big"
otherwise if x == 10
print "equal"
otherwise
print "small"
.
```

### Loops
```rawlang
loop i from 0 to 5
print i
.

loop for item in nums
print item
.
```

## Comments

```rawlang
# python style
// c style
```

## Manual code blocks

Use fenced blocks for direct code passthrough:

````rawlang
```python
print("real python code")
```
````

Accepted tags:
- target-specific: `python`, `javascript`, `golang`, `rust`
- generic passthrough: no tag, `code`, `real code`, `manual`

## Scope closing

Use a single line with `.` to close a block when needed.
