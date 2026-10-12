# NotifyIconSettings — iconos de bandeja siempre visibles (Windows 11 22H2+)

Tweak para que los íconos nuevos de la bandeja del sistema (system tray) aparezcan **activados por defecto**, sin tener que ir cada vez a *Configuración > Personalización > Barra de tareas > Otros iconos de la bandeja del sistema* a prender el switch a mano.

## El problema

Desde Windows 11 22H2, Microsoft eliminó el switch global "Mostrar siempre todos los iconos" (el viejo `EnableAutoTray` del registro se ignora). La visibilidad pasó a ser **por ícono**: cuando una app nueva registra un ícono en la bandeja, Windows lo crea **oculto** por defecto y hay que activarlo manualmente.

## Cómo lo guarda el registro

Cada ícono tiene una subclave en:

```
HKEY_CURRENT_USER\Control Panel\NotifyIconSettings\<id>\IsPromoted (DWORD)
```

- `<id>` = número uint64 generado por Windows por cada ícono registrado.
- Valores de `IsPromoted`: **ausente** = nunca tocado por el usuario (oculto por defecto); **1** = visible (On); **0** = oculto manualmente (Off).
- Esquema de cada subclave: `IconGuid`, `ExecutablePath` (ruta del exe), `IconSnapshot` (PNG del ícono), `IsPromoted`.

No existe policy de grupo ni clave global que cambie el default — la única forma es escribir `IsPromoted` por ícono.

## Qué hace este tweak

1. **`Enable-TrayIcons.ps1`** — lee todas las subclaves de `NotifyIconSettings` y promueve a `IsPromoted=1` los íconos que:
   - no tienen el valor (el usuario nunca los tocó → estaban ocultos por default), o
   - son **subclaves nuevas** (no vistas antes) que aparecieron con valor 0.

   Los íconos que el usuario desactivó a mano (0, ya conocidos) **nunca se tocan**: el script mantiene un snapshot JSON (`tray-icons-state.json`) con los IDs registrados en cada corrida para distinguir "nuevo" de "desactivado a mano". Las promociones se registran en `Enable-TrayIcons.log`.

2. **`launcher.vbs`** — invoca el `.ps1` oculto (sin ventana de consola parpadeando).

3. **Tarea programada** — corre el launcher al iniciar sesión y cada 1 minuto (costo: leer ~70 claves del registro). Así cualquier app instalada o abierta recién tiene su ícono visible en menos de un minuto.

## Instalación

1. Copiar la carpeta `NotifyIconSettings` a una ruta estable del equipo (ej. `C:\Tools\WindowsTweaks\NotifyIconSettings`).
2. Registrar la tarea programada (PowerShell, sin admin — es HKCU y tarea del usuario actual):

```powershell
$dir = 'C:\Tools\WindowsTweaks\NotifyIconSettings'   # ajustar a la ruta elegida

$action   = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "`"$dir\launcher.vbs`""
$tLogon   = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$tOnce    = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) `
              -RepetitionInterval (New-TimeSpan -Minutes 1) `
              -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
              -StartWhenAvailable -MultipleInstances IgnoreNew `
              -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

Register-ScheduledTask -TaskName 'EnableTrayIconsAutoPromote' -Action $action `
    -Trigger $tLogon,$tOnce -Settings $settings -Principal $principal -Force
```

3. Ejecutar una vez para hacer el baseline inicial:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$dir\Enable-TrayIcons.ps1"
```

La primera corrida solo registra el snapshot (promueve únicamente los íconos sin valor, que nunca los tocaste). A partir de ahí, todo ícono nuevo se activa solo.

## Desinstalación

```powershell
Unregister-ScheduledTask -TaskName 'EnableTrayIconsAutoPromote' -Confirm:$false
Remove-Item 'C:\Tools\WindowsTweaks\NotifyIconSettings' -Recurse   # ajustar ruta
```

Los archivos generados en la carpeta (`tray-icons-state.json`, `Enable-TrayIcons.log`) se borran con ella. El registro vuelve a su comportamiento default en el próximo ícono nuevo.

## Notas

- **Explorer cachea el estado promocido**: si un ícono nuevo no salta al toque, puede necesitar un re-flusheo del taskbar (o un logoff). Si ocurre seguido, se puede agregar un reinicio de `explorer.exe` automático al script — solo cuando hubo promoción.
- Si una app se actualiza y se re-registra con un **nuevo** `<id>` (común en apps MSIX/Store), vuelve a contarse como ícono nuevo y se promueve de nuevo — que es justamente el comportamiento deseado.
- El patrón `wscript.exe` + PowerShell puede disparar alertas heurísticas en EDR corporativos; en ese caso, correr el `.ps1` directamente desde la tarea (a costa de un breve parpadeo de consola).
- Compatible con Windows 11 22H2+ (probado en build 26300). En Windows 10 / 11 21H2 el mecanismo viejo (`EnableAutoTray`) sigue siendo suficiente.
