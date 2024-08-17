'''
Utilidades relacionadas a los módulos `time` y `datetime`.
'''
import threading
import time
import datetime 

def _timer(stop_event, espera:int):
    '''Bucle del timer para el thread.'''
    start = time.time()
    while not stop_event.is_set():
        actual = time.time()
        lapso = int(actual - start)
        
        print(f"En ejecución: {lapso} s", end="\n")
        
        time.sleep(espera)

def terminal_time(funcion,espera=10):
    '''
    Imprime por terminal el tiempo transcurrido mientras 
    se ejecuta a función ingresada.

    ### parámetros

    :funcion: nombre de la función que se ejecutará. 
    Usar `lambda: foo(arg)` si es necesario pasar argumentos.
    :espera: segundos de espera entre impresiones.
    '''

    stop_event = threading.Event()
    timer_thread = threading.Thread(target=_timer, args=(stop_event,espera,))
    timer_thread.start()
    
    try:
        # EJECUCIÓN
        funcion()

        stop_event.set()
        timer_thread.join()
    except KeyboardInterrupt:
        # Detener el temporizador con terminal
        stop_event.set()
        timer_thread.join()
        print("\nTemporizador detenido.")

def timestamp():
    return datetime.datetime.now()

def sleep(t):
    '''Envolutura de `time.sleep`.'''
    time.sleep(t)

class TiempoEjec:
    '''Contar intervalos temporales.
    **Inicia al instanciar**.
    
    Usar método `reset` para volver a 
    contar desde 0.
    '''
    def __init__(self) -> None:
        self.start = time.time()

    def stop(self):
        '''Retornar tiempo transcurrido.'''
        return time.time() - self.start

    def reset(self):
        ''''''
        self.start = time.time()