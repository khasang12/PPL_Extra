# premable
main:
	li $s0, 5
Label2:
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
	subi $s0, $s0, 1
	j Label2
Label3:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
