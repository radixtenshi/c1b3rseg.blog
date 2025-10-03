# Colección de Llaves de Registro para Windows

Este documento describe y explica cada archivo `.reg` que conforma una colección para ajustar privacidad, rendimiento, red, interfaz y servicios en sistemas Windows.

---
## PRIVACIDAD Y SEGURIDAD

### Cortana (`Disable Cortana.reg` / `Enable Cortana.reg`)
- Desactiva Cortana y bloquea búsquedas web. Reverso restaura funcionalidad completa.

### Privacy Values (`Disable Privacy Values.reg` / `Enable Privacy Values.reg`)
- El 'Disable' reactiva seguimiento de Bing y Cortana. El 'Enable' lo desactiva. Nombres confusos.

### Telemetry (`Disable Telemetry.reg` / `Enable Telemetry.reg`)
- Bloquea o reactiva el envío de datos diagnósticos a Microsoft.

### Compatibility Telemetry (`Disable_Compatibility_Telemetry.reg` / `Enable_Compatibility_Telemetry.reg`)
- Controla telemetría de compatibilidad. Desactivación puede afectar funciones.

### App Tracking (`Disable Windows App tracking to improve Start and Search Results.reg` / `Enable ...`)
- Habilita o desactiva historial de uso frecuente de apps.

### User Tracking (`Disable_User_Tracking.reg` / `Enable_User_Tracking.reg`)
- Supuestamente controla seguimiento de actividad del usuario.

### SmartScreen Filter (`Disable_SmartScreen_Filter.reg` / `Enable_SmartScreen_Filter.reg`)
- Desactiva protección contra sitios maliciosos. No recomendado en entornos expuestos.

### Secure Logon (`Disable_Secure_Logon.reg` / `Enable_Secure_Logon.reg`)
- Quita o requiere Ctrl+Alt+Del para iniciar sesión.

### Lock Screen (`Disable_Lock_Screen.reg` / `Enable_Lock_Screen.reg`)
- Omite o restaura la pantalla de bloqueo.

### Remote Assistance (`Disable_Remote_Assistance.reg` / `Enable Remote_Assistance.reg`)
- Impide o permite asistencia remota de terceros.

### RDP Sessions (`Disable_Concurrent_RDP_Sessions.reg` / `Enable_Concurrent_RDP_Sessions.reg`)
- Controla sesiones simultáneas por usuario en RDP.

### Take Ownership (`Take_ownership_ADD.reg` / `Take_ownership_REMOVE.reg`)
- Añade o elimina opción contextual para tomar propiedad de archivos.

### Windows Defender (`Windows_Defender_Disable.reg` / `Windows_Defender_Enable.reg`)
- Habilita o desactiva el antivirus integrado de Windows.

### Tracking Domains (`Block_Tracking_Domains.reg` / `Unblock_Tracking_Domains.reg`)
- Bloquea o desbloquea resolución de dominios de telemetría por IPv6.

---
## RENDIMIENTO Y OPTIMIZACIÓN

### Fast Startup
- Controla inicio rápido de Windows.

### Ultimate Performance
- Habilita plan de energía máximo.

### RAM/Speed Tweaks
- Ajustes de tiempo de respuesta y cierre de apps.

### System Responsiveness
- Modifica prioridad de tareas en segundo plano.

### AlwaysUnloadDLL
- Descarga DLLs no usadas para liberar memoria.

### NTFS Performance
- Controla escritura de metadatos (último acceso).

### USB Transfer Speed
- Ajusta búfer para acelerar transferencia por USB.

---
## RED Y CONECTIVIDAD

### HCDN WiFi Restriction
- Activa o elimina políticas internas de WiFi.

### Large Send Offload
- Activa o desactiva funciones avanzadas de red.

### Network Optimize
- Ajustes TCP para mejorar rendimiento de red.

### Network Adapter Max Performance
- Controla ahorro energético del adaptador.

### IPv6 Components
- Activa o desactiva completamente IPv6.

### DNS Cache
- Ajusta tamaño de caché DNS.

### Time Sync
- Controla sincronización automática de hora.

### Microsoft Edge Auto Launch / Preloading
- Evita o permite carga automática de Edge.

### Edge como buscador Google
- Reemplaza Bing por Google como motor de búsqueda.

---
## INTERFAZ Y PERSONALIZACIÓN

### App Suggestions
- Oculta o muestra sugerencias en el menú Inicio.

### Explorer Group Items
- Activa o desactiva agrupación en el Explorador.

### Folder View
- Elimina o restaura vistas por tipo de carpeta.

### Auto Arrange
- Controla ordenamiento automático de íconos.

### Tray Icons
- Muestra todos los íconos en la bandeja o los oculta.

### Explorador en Este equipo
- Fuerza que abra en 'Este equipo' en vez de Acceso rápido.

### Mostrar segundos en el reloj
- Añade segundos al reloj del sistema.

### Ejecutar como otro usuario
- Añade opción contextual para ejecución como otro usuario.

### Panel y Mezclador Clásicos
- Restaura Panel de control y Mezclador antiguos.

---
## SISTEMA Y SERVICIOS

### Windows Update
- Activa o desactiva las actualizaciones automáticas.

### Windows Defender
- Habilita o desactiva antivirus integrado.

### Indexado de búsqueda
- Controla servicio de indexado.

### AutoPlay
- Controla reproducción automática de medios.

### Fast Disk Cleanup
- Activa versión rápida del liberador de espacio.

### Sticky Keys
- Activa o elimina atajos de accesibilidad.

### UAC Prompt
- Controla el comportamiento de confirmación de administrador.

### Lid Close Behavior
- Controla qué pasa al cerrar la tapa de una notebook.

### SMBv1
- Habilita o desactiva protocolo SMBv1 (obsoleto).

### Explorer Features
- Activa o elimina funciones visuales modernas.

### System Responsiveness (único)
- Desactiva reserva de CPU para tareas en segundo plano.