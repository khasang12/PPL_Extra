# premable
main:
	li $s0, 5
	li $s0, 5
Label4:
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
Label5:
	li $s1, 0
	li $s1, 2
Label10:
	li $t0, 0
	sub $t0, $s1, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label9
Label11:
	subi $s1, $s1, 1
Label8:
Label12:
	subi $s1, $s1, 1
	j Label10
Label9:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
Label2:
Label6:
	subi $s0, $s0, 1
	j Label4
Label3:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
