signos_admitidos=['+','-','*','/'];
def search(str_,list_char,start=0):
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
    search_parenthesis(str_,start=0,end=None);
    Busca el inicio y el fin de un parentesis,
        innorando los que sean hijos o decen-
        diente del parentesis origina: "(())"
         retorna [0,3].
    
    Example:
    >>> search_parenthesis("hola(como ((estas)) )");
        [4, 20]
    Comprueba si el primer parentesis quedo abierto,
        en ese caso retorna -1.
    
    Example:
    >>> search_parenthesis("hola(como ((estas) )");
        -1
    Pero no comprueba si se cierra mas parentesis de
        los que se abre:
    
    Example:
    >>> search_parenthesis("hola(como ((estas)) ) )");
        [4, 20]
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

def get_num_of_str(str_):
    """
    get_num_of_str(str_);
        Funcion que retorna el numero pasado por la cadena, ya sea float o int retorna el numero.
    """
    l=search(str_,['.',',']);
    if l['.']!=None:
        return float(str_);
    elif l[',']!=None:
        return float(str_[ : l[','][0] ]+'.'+str_[ l[','][0]+1 : ]);#Ajuro debemos convertir ese signo para que la funcion float no lo vea como un string.
    else:
        return int(str_);
def calculation(a,operator,b):#No tratare de tratar errores en esta funcion para asegurar velocidad.
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
def Calculator(str_input):
    class Error_arg(Exception):
        def __init__(self,msg="Error: The argument must only be str. Example: Cacular('1+1');"):
            self.message=msg;
    is_negative=False;#Solo afectara al primer numero convirtiendolo en negativo.
    i=0;#indice, lo coloco aqui para poder cambiarlo con el elif.
    if not isinstance(str_input,str):
          raise Error_arg;
    if str_input[0] in signos_admitidos:#Nos aseguramos de tratar como se debe al primer signo que introduce el usuario.
        if str_input[0]=='/':
            raise SyntaxError( "Operation not valid: '/' "+str_input[1:] );
        elif str_input[0]=='-':
            is_negative=True;
        str_input=str_input[1:];
    result=0;
    num=[];
    operand=[];
    str_="";
    flags={"previous":False,"if a number":True,"pre_is_parenthesis":False};
    i=0;
    STR_LEN=len(str_input);
    while i<STR_LEN:
        char=str_input[i];
        if char in signos_admitidos:
            if flags["previous"]:#Normal: 2+2
                num.append(get_num_of_str(str_));
                operand.append(char);
                """Aqui creo otro flag para saber si es multipricacion
                    Si lo es no se trata el numero siguiente como normalmente
                    se quita el numero anterior y se trata con el numero actual como se debe: get_num_of_str(1)*get_num_of_str(2)
                """
            else:
                """No deberia ser necesario: if not flags["pre_is_parenthesis"]:
                    flags["pre_is_parenthesis"]=False;
                    continue;"""
                if char=='-' or char=='-':#Entoces el numero es negativo.
                    is_negative=(char=='-');
                else:
                    raise SyntaxError("Operation not valid.");
            
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
    MAX_NUM=len(num);
    MAX_OPERAND=len(operand);
    #Por si el usuario ingreso dos numeros:
    if MAX_NUM==1:
        if MAX_OPERAND==0 or len(str_)==0:#Solo ingreso un numero.
            return num[0];
        else:#Ingreso los dos.
            return calculation(num[0],operand[0],get_num_of_str(str_));
    elif MAX_NUM==0:#Vemos si ingreso solo un numero:
        return get_num_of_str(str_) if len(str_)>0 else 0;#Si ingreso solo un signo retornamos 0.
    
    #Para asegurarme que puse todos los numeros:
    if not len(str_)==0:
        num.append(get_num_of_str(str_));
    #if DEBUG:
    # print("str_: "+str_+", char: "+char+", i: "+str(i)+", str_input: "+str_input+", num: ",num);
    # print("operand: ",operand);
    del i , STR_LEN , str_ , str_input;
    """TODO: Arreglar: El tratado de los signos:
                2*-4 o 3*+4
              Tambien debo agregar la regla de la
              multipricacion de signos.
        TODO: Debes hacer una documentacion a la funcion search
            y traducir a ingles todas las demas documentaciones.
    """
    #if DEBUG:
    # print("str_input: "+str_input+", num: ",num);
    # print("str_input: "+str_input+", sign: ",operand);
    result=-1*num[0] if is_negative else num[0];
    i_s=0;
    MAX_NUM=len(num);
    if '*' in operand:#Tratamos primero al signo de multipricacion.
        i=0 ;
        i_s_l=0;
        #i: indice, s: signo, l: local.
        while i_s_l<MAX_OPERAND:
            if operand[i_s_l]=='*':
                n_delete=0;
                
                if i+1<MAX_NUM:#Si el numero de elementos de la lista es par.
                    num[i]=num[i]*num[i+1];
                    n_delete=i+1;
                elif i!=MAX_NUM:#Si no.
                    
                    num[i-1]=num[i-1]*num[i];
                    n_delete=i;
                else:
                    num[i-2]=num[i-1]*num[i-2];
                    n_delete=i-1;
                
                del operand[i_s_l],num[n_delete];#Liberamos los espacios asignados.
                
                MAX_OPERAND-=1;#Actualizamos nuestro indice.
                MAX_NUM-=1;
                
                i_s_l=-1;#No estoy muy seguro como obtimizar esto.
                i=0;
            if i+1<MAX_NUM:
                i+=2;
            i_s_l+=1;
            
        del i,i_s_l;
    
    for i_n in range(1,len(num)):
        n_2=num[i_n];
        if i_s<MAX_OPERAND:
            result=calculation(result,operand[i_s],n_2);
            i_s+=1;
        else:#Ocurrio un error inesperado.
            raise NameError("Error inesperado de la apricacion.");
    #if DEBUG:
    # print("Result: "+str(result));
    return result;


if __name__=="__main__":
    DEBUG=True;
    if DEBUG:
        from timeit import timeit;
    """operation="1+1-(2+3+(1-1))*(1+(2-3-4))*4";#Da 12 porque pase por alto que primero se multiprica y despues se saca lo demas.
    print("operacion con python: "+str(1+1-(2+3+(1-1))*(1+(2-3-4))*4));
    print(operation+": ",Calculator(operation));
    operation="123+";
    #print(operation+": ",Calculator(operation));
    """
    input_='';
    while True:
        input_=input("Ingrese su operacion para sacar el calculo:\n --> ").lower();
        if input_=='q':
            break;
        print("Operacion con python: ",end="");
        timeit(f"print({input_});",number=1);
        print("Operacion com mi calculadora: "+str());
