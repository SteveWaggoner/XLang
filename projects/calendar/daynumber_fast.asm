;
; File generated by cc65 v 2.19 - Git d1bf3ba8c
;
	.fopt		compiler,"cc65 v 2.19 - Git d1bf3ba8c"
	.setcpu		"65C02"
	.smart		on
	.autoimport	on
	.case		on
	.debuginfo	off
	.importzp	sp, sreg, regsave, regbank
	.importzp	tmp1, tmp2, tmp3, tmp4, ptr1, ptr2, ptr3, ptr4
	.macpack	longbranch
	.import		_printf
	.export		__dayNumberFast






; ---------------------------------------------------------------
; unsigned char __near__ dayNumberC (unsigned char day, unsigned char month, unsigned short year)
; ---------------------------------------------------------------

.segment	"CODE"

.proc	__dayNumberFast: near

.segment	"CODE"

	jsr     pushax

    ;
    ; print day
    ;
	lda     #<(S0001)
	ldx     #>(S0001)
	jsr     pushax
	ldy     #$05
	ldx     #$00
	lda     (sp),y
	jsr     pushax
	ldy     #$04
	jsr     _printf


    ;
    ; print month
    ;
	lda     #<(S0002)
	ldx     #>(S0002)
	jsr     pushax
	ldy     #$04
	ldx     #$00
	lda     (sp),y
	jsr     pushax
	ldy     #$04
	jsr     _printf


    ;
    ; print year
    ;
	lda     #<(S0003)
	ldx     #>(S0003)
	jsr     pushax
	ldy     #$03
	jsr     ldaxysp
	jsr     pushax
	ldy     #$04
	jsr     _printf


    ;
    ; print day/month/year
    ;

	lda     #<(S0004)
	ldx     #>(S0004)
	jsr     pushax
	ldy     #$05
	ldx     #$00
	lda     (sp),y
	jsr     pushax
	ldy     #$06
	ldx     #$00
	lda     (sp),y
	jsr     pushax
	ldy     #$07
	jsr     ldaxysp
	jsr     pushax
	ldy     #$08
	jsr     _printf


    ;
    ; year -= month < 3;
    ;

	ldy     #$02
	lda     (sp),y   ; copy month to a
	cmp     #$04
    bcs     month_greater_than_3
   
    ; decrement year by one
	ldy     #$00
	ldx     #$00
    lda     (sp), y   ; low byte
    sec               ; why set this to get substract to work correctly?
    sbc     #1
    sta     (sp), y   ; low byte
    iny 
    lda     (sp), y   ; high byte
    sbc     #0         
    sta     (sp), y   ; high byte

  month_greater_than_3:



    ;
    ; tmp = year;
    ;

	ldy     #$00
    lda     (sp), y   ; low byte
    sta     M0001     ; low byte
    iny 
    lda     (sp), y   ; high byte
    sta     M0001+1   ; high byte

    ;
    ; tmp = tmp + year / 4;
    ;
	lda     M0001
	ldx     M0001+1


	jsr     pushax    ; push ax to stack
	ldy     #$03
	jsr     ldaxysp   ; copy sp+3 to ax 
	jsr     shrax2    ; divide ax by 4
	jsr     tosaddax  ; top of stack add to ax (pop 2 bytes)
	sta     M0001
	stx     M0001+1

    ;
    ; tmp = tmp - year / 100;
    ;
	lda     M0001
	ldx     M0001+1
	jsr     pushax
	ldy     #$03
	jsr     ldaxysp
	jsr     pushax
	ldx     #$00
	lda     #$64
	jsr     tosudivax
	jsr     tossubax
	sta     M0001
	stx     M0001+1

    ;
    ; tmp = tmp + year / 400;
    ;
	lda     M0001
	ldx     M0001+1
	jsr     pushax
	ldy     #$03
	jsr     ldaxysp
	jsr     pushax
	ldx     #$01
	lda     #$90
	jsr     tosudivax
	jsr     tosaddax
	sta     M0001
	stx     M0001+1

    ;
    ; tmp = tmp + t[month - 1];
    ;
	lda     M0001
	ldx     M0001+1
	jsr     pushax

	ldy     #$04
	ldx     #$00
	lda     (sp),y
	jsr     decax1
	clc
	adc     #<(M0002)
	tay
	txa
	adc     #>(M0002)
	tax
	tya
	ldy     #$00
	jsr     ldauidx

	jsr     tosaddax
	sta     M0001
	stx     M0001+1

    ;
    ; tmp = tmp + day;
    ;
	lda     M0001
	ldx     M0001+1
	jsr     pushax
	ldy     #$05
	ldx     #$00
	lda     (sp),y
	jsr     tosaddax
	sta     M0001
	stx     M0001+1

    ;
    ; return tmp % 7;
    ;
	lda     M0001
	ldx     M0001+1
	jsr     pushax
	ldx     #$00
	lda     #$07
	jsr     tosumodax
	ldx     #$00
	jmp     L0001
L0001:	jsr     incsp4
	rts

.segment	"DATA"

M0001:
	.word	$0000
M0002:
	.byte	$00
	.byte	$03
	.byte	$02
	.byte	$05
	.byte	$00
	.byte	$03
	.byte	$05
	.byte	$01
	.byte	$04
    .byte	$06
	.byte	$02
	.byte	$04

S0004:
	.byte	$44,$4D,$59,$3D,$25,$44,$2F,$25,$44,$2F,$25,$44,$0D,$00
S0002:
	.byte	$4D,$4F,$4E,$54,$48,$3D,$25,$44,$0D,$00
S0003:
	.byte	$59,$45,$41,$52,$3D,$25,$44,$0D,$00
S0001:
	.byte	$44,$41,$59,$3D,$25,$44,$0D,$00

.endproc

