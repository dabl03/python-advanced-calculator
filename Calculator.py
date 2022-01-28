signos_admitidos=['+','-','*','/'];
def search(list_char,str_,start=0):
    """
---------------------------------------------------------
|   Busca un char ingresado por list_char en una 
|   | cadena pasada por str_, Cuando lo consige
|   | crea una lista con la ubicacion de todas 
|   | las coincidencia y lo guarda en una lista.
|   |
|   return: {char_1:[coincidencia],....}.
|   |
|   example:
|   | >> search(['+','-','*','/'],"1-2-3+4+5*6*7*8+9*7");
|   |   {'+': [5, 7, 15], '-': [1, 3], '*': [9, 11, 13, 17], '/': None}
---------------------------------------------------------
    """
    if not isinstance(str_,str):
        raise ValueError("I do not pass a chain as an argument");
    coincidence={};
    for a in list_char:
        coincidence.update({a:[]});
        is_list_empit=True;
        for b in range(start,len(str_)):
            if a==str_[b]:
                coincidence[a].append(b);
                is_list_empit=False;
        if is_list_empit:#To know if it is an empty list.
            coincidence[a]=None;
    return coincidence;

def search_parenthesis(str_,start=0,end=None):
    """
-------------------------------------------------------
|   Busca el inicio y el fin de un parentesis,
|   |  innorando los que sean hijos o decen-
|   |  diente del parentesis origina: "(())"
|   |  retorna [0,3].
|   Example:
|   |  >>> search_parenthesis("hola(como ((estas)) )");
|   |      [4, 20]
|   Nota: Comprueba si el primer parentesis quedo 
|   |  abierto, en ese caso retorna -1.
|   |  Example:
|   |  | >>> search_parenthesis("hola(como ((estas) )");
|   |  |    -1
|   |  Pero no comprueba si se cierra mas 
|   |  parentesis de los que se abre.
--------------------------------------------------------
    """
    
    LEN=len(str_);#For higher speed.
    #Comprobamos que ingreso un buen dato final.
    if not isinstance(end,int):
        end=LEN;
    elif end > LEN or end<0:
        end=LEN;
    del LEN;#Desde aqui ya no se necesita.
    
    i_parenthesis=0;
    init_end=[0,0];
    
    for i in range(start,end):
        if str_[i]=='(' or str_[i]==')':
            if str_[i]=='(':
                if i_parenthesis==0:#Si es el inicio marcamos la ubicacion inicial.
                    init_end[0]=i;
                i_parenthesis+=1;
            else:
                i_parenthesis-=1;
                if i_parenthesis==0:#Si es el final marcamos esta ubicacion y retornamos las coordenadas.
                    init_end[1]=i;
                    return init_end;
    return -1;#Si no se encontro el parentesis final entonces retornamos -1.

def get_num_of_str(str_) -> str:
    """
------------------------------------------
|   Funcion que retorna el numero pasado 
|   | por la cadena, ya sea float o int.
|   example:
|   | >> get_num_of_str("12")
|   |   12
|   | >> get_num_of_str("12,3")
|   |   12.3
|   | >> get_num_of_str("12.3")
|   |   12.3
--------------------------------------------
    """
    l=search(['.',','],str_);
    if l['.']!=None:
        return float(str_);
    elif l[',']!=None:
        return float(str_[ : l[','][0] ]+'.'+str_[ l[','][0]+1 : ]);#Ajuro debemos convertir ese signo para que la funcion float no lo vea como un string.
    else:
        return int(str_);
def calculation(a,operator,b):#No tratare de tratar errores en esta funcion para asegurar velocidad.
    """
-----------------------------------------------------
|   Funcion que toma 1 numero, un string y 1 numero.
|   | con esos numeros usa el string para retorna 
|   | una operacion matematica.
|   |   
|   Example:
|   | >> calculation(2,'*',2);
|   |    4
|   Return: int or float or None.
-------------------------------------------------------
    """
    if operator=='+':
        return a+b;
    elif operator=='-':
        return a-b;
    elif operator=='*':
        return a*b;
    elif operator=='/':
        return a/b;
    else:#No es necesario.
        return None;
def Calculator(str_input) -> str:
    """
---------------------------------------------------------
|   Motor para calculadora avanzadas, diseñada
|   | para hacer operaciones dificiles
|   | como: 1-2-3+4+5*6*7*8+9*7*(-1-3*4).
|   | Esta diseñada para tratar errores como 1*
|   |  o 1************************
|   |  o 1*************************1
|   |  y sacar el resultado.
|   |
|   Example:
|   | >> 1-2-3+4+5*6*7*8+9*7*(-1-3*4)
|   |   861
|   return: int or float.
|   Nota: Todavia no saca potencia, raiz cuadrada y tam-
|   |  poco tiene contantes como PI.
|   | para ver lo que puede hacer: ver la lista
|   |   de signos admitidos(signos_admitidos).
---------------------------------------------------------
    """
    class Error_arg(Exception):
        def __init__(self,msg="Error: The argument must only be str. Example: Cacular('1+1');"):
            self.message=msg;
    is_negative=False;#Solo afectara al primer numero convirtiendolo en negativo.
    i=0;#indice, lo coloco aqui para poder cambiarlo con el elif.
    if not isinstance(str_input,str):
          raise Error_arg;
    if len(str_input)==0:
        return 0;
    if str_input[0] in signos_admitidos:#Nos aseguramos de tratar como se debe al primer signo que introduce el usuario.
        if str_input[0]=='/':
            raise SyntaxError( "Operation not valid: '/' "+str_input[1:] );
        elif str_input[0]=='-':
            is_negative=True;
        str_input=str_input[1:];
    num=[];
    operand=[];
    str_="";
    flags={"previous":False,"is_":""};
    i=0;
    MAX_NUM=0;
    MAX_OPERAND=0;
    STR_LEN=len(str_input);
    while True:
        if i>=STR_LEN:
            if len(str_)>0:
                num.append(get_num_of_str(str_));
            MAX_NUM=len(num);
            MAX_OPERAND=len(operand);
            
            #Por si el usuario no ingreso numeros:
            if MAX_NUM==0:
                return 0;
            elif MAX_NUM==1:#Por si el usuario ingreso 1 numero:
                return num[0];
            elif MAX_NUM==2:#Ingreso dos numeros.
                if MAX_OPERAND==0:#Si estuvo un signo de multipricacion o division ya se habra eliminado, pero falta hacer la operacion.
                    return num[0]*num[1] if flags["is_"]=='*' else num[0]/num[1];
                return calculation(num[0],operand[0],num[1]);
            #Si el ultimo es multipricacion o division:
            if  not flags["is_"]=="":#Recuerda primero se hace la multipricacion.
                num[-2]=num[-2]*num[-1] if flags["is_"]=='*' else num[-2]/num[-1];
                del num[-1];
            break;
        char=str_input[i];
        if char in signos_admitidos:
            if flags["previous"]:#Normal: 2+2
                if  not flags["is_"]=="":#Recuerda primero se hace la multipricacion.
                    num_2=get_num_of_str(str_);
                    num[-1]=num[-1]*num_2 if flags["is_"]=='*' else num[-1]/num_2;
                    flags["is_"]="";
                else:
                    num.append(get_num_of_str(str_));
                #Recuerda que la multipricacion y division se hacen primeros que las sumas y restas.
                #El flags es porque actualmente no conosco el numero, pero despues si lo conocere.
                if char=='*' or char=='/':
                    flags["is_"]='*' if char=='*' else '/';
                else:
                    operand.append(char);
            else:
                if char=='-' or char=='-':#Entoces el numero es negativo.
                    is_negative=(char=='-');
                else:
                    #Cuando pase:
                    #    --> 2**  retorna: 2
                    #    --> 2**2 retorna 2*2 o 4
                    #    --> 2/*2 retorna 2*2 o 4
                    #    --> 2*/2 retorna 2/2 o 1
                    #"""Se tomara el ultimo signo: Nota: Si quieres que pase el primer signo pon esto en comentario:{
                    if char=='*' or char=='/':
                        flags["is_"]='*' if char=='*' else '/';
                    #}"""
                    pass;
            
            str_="";
            flags["previous"]=False;
        elif char=='(':
            l=search_parenthesis(str_input,i);
            if isinstance(l,int):#Si se retorno -1 entonces no se ha cerrado el parentesis.
                num.append(Calculator( str_input[i+1:] ));
                break;
            str_=str( Calculator(str_input[ i+1:l[1] ]) );
            #tambien es valido: num[a_or_b].append(Cacular( str_input[ l[0]+1:l[1] ] ));
            i=l[1];
            flags["previous"]=True;
            #flags["pre_is_parenthesis"]=True;
        else:
            str_+=char;
            flags["previous"]=True;
            if is_negative:
                str_='-'+str_;
                is_negative=False;
        i+=1;
        
    # Creo que no es necesario, ¿sera que lo quito?:
    del i , STR_LEN , str_ , str_input, is_negative, flags;
    
    i_s=0;
    result=num[0];
    for i_n in range(1,len(num)):
        n_2=num[i_n];
        if i_s<MAX_OPERAND:
            result=calculation(result,operand[i_s],n_2);
            i_s+=1;
        else:#Ocurrio un error inesperado.
            print(f"num: {num}, operand: {operand}, i_s: {i_s}");
            raise NameError("Error inesperado de la apricacion.");
    return result;


if __name__=="__main__":
    """
        Para saber si funciona la Calculadora comparamos su resultados con los resultados de python.
    """
    from timeit import timeit;
    input_='';
    comparar=True;
    while True:
        input_=input(f"""
        Ingrese 'q' para terminar.\n
        Ingrese 'n' para calcular sin comparar con python.\n
        Ingrese su operacion para sacar el calculo:
comparar={comparar}
 --> """).lower();
        if input_[0]=='q':
            break;
        elif input_[0]=='n':
            comparar=False;
            continue;
        if comparar:
            print("Operacion con python: ",end="");
            timeit(f"print({input_});",number=1);
        print("Operacion com mi calculadora: "+str(Calculator(input_)));
        """Nota: Si una formula se calculo mal por mi calculadora entonces por favor rellena este formulario y enviamelo:
            ERROR: ?
            Resultado obtenido: ?
            Resultado deseado: ?
        """
    input("Enter space for finish.");
#Nota: La calculadora de window al sacar esta cuenta: 2*2+2-4+6*7+8*6+3/2/3 me retorna 64.5, pero el shell de python y la calculadora de mi telefono me retorna 92.5, digo shell porque no saque la cuenta con mi calculadora.
