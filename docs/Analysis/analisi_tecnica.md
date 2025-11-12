# ANALISI TECNICA

## Comunicazione robot <-> pc

Per realizzare la comunicazione tra il robot e il PC è stato implementato un server HTTP hostato in locale sul computer.
Il robot, a ogni evento significativo della linea di produzione, effettua una richiesta HTTP POST verso il server, inviando un payload in formato JSON contenente i dati dell’operazione eseguita (ad esempio stato sensori, coordinate o esito delle azioni).

Il server riceve questi dati e li inoltra immediatamente alla piattaforma ThingsBoard mediante una richiesta HTTP, permettendo così il monitoraggio in tempo reale del sistema tramite dashboard IoT.

## Codice robot

Il software a bordo dei robot è progettato per:

1. Gestire le operazioni del robot sui materiali della linea di produzione.
2. Eseguire il reporting automatico delle azioni completate al server locale.

Per ogni robot abbiamo creato delle funzioni che aiutano alla programmazione.
Per il dobot magician:

```python
def get_sensor_status() -> int:
  """
  Gets the infrared sensor status

  Returns
  ------
  int
    0 if the sensor doesn't detect anything
    1 if the sensor detect anything
  """
  return magicbox.get_infrared_sensor(port=2)["status"] # type: ignore
```

```python
def move_to_point(p: Point, mode: int = 0):
  """
  Move the robot to the coordinate of the Point with a mode

  Params
  ------
  p : Point
    The destination Point
  mode : int
    Specify the mode of movement:
      - 0: make a "jump" from the current position of the robot and the destination point
      - 1: go strait to the destination point
  """
  magician.ptp(mode, p.x, p.y, p.z, 0) # type: ignore
```

```python
def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """
  Move the robot to the coordinate of the Point and the offset with a mode.

  Params
  ------
  p : Point
    The destination Point
  off_x : float
    The offset to apply to the x of the destination point
  off_y : float
    The offset to apply to the y of the destination point
  off_z : float
    The offset to apply to the z of the destination point
  mode: int
    Specify the mode of movement:
      - 0: make a "jump" from the current position of the robot and the destination point
      - 1: go strait to the destination point
  """
  magician.ptp(mode, p.x + off_x, p.y + off_y, p.z + off_z, 0) # type: ignore
```

```python
def set_conv_speed(speed: int):
  """
  Set the conveyor speed.

  Params
  ------
  speed : int
    The speed to set to the conveyor.
  """
  magicbox.set_converyor(index=magicbox.STP1,enable=True,speed=speed) # type: ignore
```

```python
def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore
```

Per i dobot magician lite:

```python
def move_to_point(p: Point, mode: int = 0):
  m_lite.set_ptpcmd(ptp_mode=mode, x=p.x, y=p.y, z=p.z, r=0)# type: ignore
```

```python
def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  m_lite.set_ptpcmd(ptp_mode=mode, x=p.x + off_x, y=p.y + off_y, z=p.z + off_z, r=0) # type: ignore
```

```python
def suck(state: bool):
  m_lite.set_endeffector_suctioncup(enable=state, on=state) # type: ignore
```

## Codice server

Il server è implementato come web server locale all’interno della rete.
La sua funzione principale è ricevere le richieste HTTP inviate dai robot, elaborare i payload JSON e inoltrarli a ThingsBoard o ad altri endpoint interni.

Torna all'[analisi funzionale](./analisi_funzionale.md)

Torna al [README](../../README.md)
