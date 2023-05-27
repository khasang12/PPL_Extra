# premable
main:
	li $s0, 0
Label4:
	li $t0, 5
	sub $t0, $s0, $t0
	slt $t1, $t0, $zero
	beq $t1, $zero, Label3
Label5:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
Label2:
Label6:
	addi $s0, $s0, 1
	j Label4
Label3:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
