## 1. Настройка доступа по публичному IP
### 1.1 Заходим в веб-интерфейс по адресу 192.168.1.1 , нажимаем "Далее" до момента "Выйти из настройки", нажимаем туда. 
<img src='Pasted image 20260512095248.png'>

### 1.2 Задаем пароль администратора, нажимаем "Далее"
![[Pasted image 20260508122128.png]]
### 1.3 Заходим в "Управление" - "Пользователи и доступ", находим секцию "Службы управления", меняем порт SSH, в секции "Удаленное управление" включаем "Удаленный доступ к веб-конфигуратору" HTTP и HTTPS, "Разрешить доступ из интернета" - по Telnet, по SSH и сохраняем
![[Pasted image 20260508122513.png]]

### Аналогичная ситуация со вторым роутером.

# 2. Настройка роутеров
### Заходим в "Статус" - "Системный монитор". Смотрим публичный IP-адрес. В моем случае R1 имеет ip - 192.168.117.44, R2 имеет ip - 192.168.117.43
![[Pasted image 20260512100027.png]]
### Первое что делаем - задаем hostname. "Управление" - "Настройки системы" - "Имя системы", задаем имя системы в соответствии с заданием.
![[Pasted image 20260508123436.png]]
### Заходим в "Мои сети и Wi-Fi" - "Гостевая сеть" и удаляем сегмент.
![[Pasted image 20260512100645.png]]
### На R1 создаем сегменты сети в соответствии с заданием, задаём ip-адреса.
![[Pasted image 20260512101731.png]]
### Листаем ниже и находим "Порты и VLAN"
### На R1 порт 1 обслуживает сегмент CAMS, порт 2 обслуживает сегмент SERVERS
![[Pasted image 20260508124812.png]]
### На R2 переходим "Мои сети и Wi-Fi" - "Гостевая сеть"
### На R2 порт 1 обслуживает сегмент ADMINS, порт 2 обслуживает сегмент PRINTERS. 
![[Pasted image 20260508125202.png]]
### Важно обратить внимание, DHCP-сервер будет включен только в сегменте ADMINS
![[Pasted image 20260508125449.png]]

### Создание GRE туннеля
#### Заходим в "Сетевые правила" - "Межсетевой экран"
![[Pasted image 20260512103231.png]]
### Нажимаем "Добавить правило" для разрешения ssh подключений по 22 и 222 портам.
![[Pasted image 20260512103427.png]]
![[Pasted image 20260512103635.png]]
![[Pasted image 20260512103715.png]]
#### Заходим через программу PuTTY на роутер по порту, который мы указывали (2022)
![[Pasted image 20260512104125.png]]
### Входим с учетными данными admin, пароль, который вы указывали в шаге 1.2
![[Pasted image 20260512104253.png]]
### Cоздаем туннель, задаем ip, указываем назначение, задаем security-level, даем возможность обмена трафиком между всеми private интерфейсами.
![[Pasted image 20260512104635.png]]
```
interface Gre0
tunnel destination 192.168.117.44
ip address 10.10.10.2 255.255.255.252
security-level private
up
exit
no isolate-private
system configuration save
```
### Аналогично делаем это на r2, меняя назначение и ip.
![[Pasted image 20260512104946.png]]
### После чего проверяем ping по туннелю
### Заходим в "Управление" - "Диагностика"
![[Pasted image 20260512105106.png]]
![[Pasted image 20260508132314.png]]
# OSPF
### Переходим в "Управление" - "Настройка системы" и "Изменить набор компонентов"
![[Pasted image 20260512105507.png]]
### Скачиваем компоненты ОС
![[Pasted image 20260512105743.png]]
![[Pasted image 20260512105834.png]]
![[Pasted image 20260512105917.png]]
### Скачиваем mipsel-installer.tar.gz с сайта https://support.keenetic.ru/giga/kn-1011/ru/20980-installing-the-entware-repository-on-a-usb-drive.html?ysclid=mp2ccka3po933064212
![[Pasted image 20260512110119.png]]
### Командой lsblk смотрим подключенные устройства, среди них находим наш флеш-накопитель,  с помощью команды umount /dev/sda размонтируем флеш-накопитель, вставленный в ПК, после чего командой /usr/sbin/mkfs.ext4 /dev/sda форматируем флеш-накопитель в файловую систему EXT4.
![[Pasted image 20260512110759.png]]
### Форматируем флеш-накопитель в EXT4, вставляем в роутер. Заходим в "Управление" - "Приложения", выбираем вставленный флеш-накопитель, через веб-интерфейс роутера создаем папку, называем install, закидываем архив mipsel-installer.tar.gz
![[Pasted image 20260512112324.png]]
![[Pasted image 20260512112604.png]]
### После чего заходим в "Управление" - "OPKG", выбираем накопитель, после чего нажимаем "Сохранить" и ждем завершения установки, заходим в "Диагностика" - "Показать журнал", там отображаются все действия по установке Entware.
![[Pasted image 20260508135830.png]]
![[Pasted image 20260512112847.png]]
### В конечном итоге получаем сообщение "Установка системы пакетов "Entware" завершена! Не забудьте сменить пароль и номер порта!"
![[Pasted image 20260508140112.png]]
# АНАЛОГИЧНО ДЕЛАЕМ НА R2.
### Через программу PuTTY подключаемся по ssh по порту 222, с учетными данными login: root, password: keenetic, скачиваем пакеты bird2 bird2c, предварительно обновляя репозитории.
![[Pasted image 20260508141232.png]]
```
opkg update
opkg install bird2
opkg install bird2c
```
### Через редактор vi удаляем всю конфигурацию /opt/etc/bird.conf, заменяя ее на эту:
### R1:
``` R
log syslog all;

router id 10.10.10.1;

protocol device {
    scan time 10;
}

protocol direct direct4 {
    ipv4;
    interface "*";
}

filter export_r1_to_ospf {
    if net = 172.16.10.0/24 then accept;
    if net = 172.16.110.0/24 then accept;
    if net = 10.10.10.0/30 then accept;
    reject;
}

filter import_from_ospf {
    if net = 172.16.120.0/24 then accept;
    if net = 172.16.100.0/24 then accept;
    reject;
}

protocol kernel kernel4 {
    ipv4 {
        import none;
        export all;
    };
    scan time 20;
    persist;
}

protocol ospf v2 ospf_gre {
    ipv4 {
        import filter import_from_ospf;
        export filter export_r1_to_ospf;
    };

    area 0.0.0.0 {
        interface "ngre0" {
            type ptp;
            cost 10;
            hello 10;
            dead count 4;
            authentication cryptographic;
            password "abi2026" {
                id 1;
            };
        };
    };
}
```
### R2:
```R
log syslog all;

router id 10.10.10.2;

protocol device {
    scan time 10;
}

protocol direct direct4 {
    ipv4;
    interface "*";
}

filter export_r2_to_ospf {
    if net = 172.16.120.0/24 then accept;
    if net = 172.16.100.0/24 then accept;
    if net = 10.10.10.0/30 then accept;
    reject;
}

filter import_from_ospf {
    if net = 172.16.10.0/24 then accept;
    if net = 172.16.110.0/24 then accept;
    reject;
}

protocol kernel kernel4 {
    ipv4 {
        import none;
        export all;
    };
    scan time 20;
    persist;
}

protocol ospf v2 ospf_gre {
    ipv4 {
        import filter import_from_ospf;
        export filter export_r2_to_ospf;
    };

    area 0.0.0.0 {
        interface "ngre0" {
            type ptp;
            cost 10;
            hello 10;
            dead count 4;
            authentication cryptographic;
            password "abi2026" {
                id 1;
            };
        };
    };
}
```
### Запускаем bird
```
/opt/etc/init.d/S70bird restart
```
### Проверяем соседство
```
birdc show ospf neighbors
```
### Проверяем маршруты
```
birdc show route
```
![[Pasted image 20260512115233.png]]
