# premable
main:
	li $s0, 0
Label2:
	addi $s0, $s0, 1
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $t0, $zero
	beq $t1, $zero, Label3
	j Label2
Label3:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
