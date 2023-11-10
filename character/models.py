from django.db import models
import glob
from os import listdir
from os.path import isfile, join
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Party(models.Model):
    party_name = models.TextField()


class ARace(models.Model):
    STR = "str"
    AGI = "agi"
    INT = "int"
    SPI = "spi"
    CNS = "cns"
    CHA = "cha"
    LUK = "luk"
    img = models.TextField()
    name = models.TextField()
    rstat = models.TextField(choices=((STR, "Siła"),
                                     (AGI, "Zręczność"),
                                     (INT, "Inteligencja"),
                                     (SPI, "Duchowość"),
                                     (CNS, "Kondycja"),
                                     (CHA, "Charyzma"),
                                     (LUK, "Szczęście")
                                     ))
    description = models.TextField()
    race_skills = models.ManyToManyField('character.Skill',symmetrical=False,related_name='raceswhoknow')


class AClass(models.Model):
    STR = "str"
    AGI = "agi"
    INT = "int"
    SPI = "spi"
    CNS = "cns"
    CHA = "cha"
    LUK = "luk"
    img = models.TextField()
    name = models.TextField()
    mstat = models.TextField(choices=((STR, "Siła"),
                                     (AGI, "Zręczność"),
                                     (INT, "Inteligencja"),
                                     (SPI, "Duchowość"),
                                     (CNS, "Kondycja"),
                                     (CHA, "Charyzma"),
                                     (LUK, "Szczęście")
                                     ))
    sstat = models.TextField(choices=((STR, "Siła"),
                                     (AGI, "Zręczność"),
                                     (INT, "Inteligencja"),
                                     (SPI, "Duchowość"),
                                     (CNS, "Kondycja"),
                                     (CHA, "Charyzma"),
                                     (LUK, "Szczęście")
                                     ))
    description = models.TextField()
    class_skills= models.ManyToManyField('character.Skill',symmetrical=False,related_name='classeswhoknow')

class CharSkill(models.Model):
    character=models.ForeignKey('character.Adventurer',on_delete=models.CASCADE,null=False,blank=False)
    proficiency = models.PositiveSmallIntegerField(default=1)

class Skill(models.Model):
    atype = models.BooleanField(default=True)
    skill_value_damage=models.PositiveSmallIntegerField(default=0,null=True)
    skill_value_heal = models.PositiveSmallIntegerField(default=0,null=True)
    skill_school=models.TextField(choices=[(x,x) for x in ['ogień','woda','mrok','światło','fizyczne','grom','magia']])
    skillimage = models.TextField(default='Icon.1_01.png')
    skill_description = models.TextField()

class Quest(models.Model):
    adventurer = models.ForeignKey('character.Adventurer',on_delete=models.CASCADE,null=True)
    name=models.TextField()
    image=models.TextField()
    description=models.TextField()
    reward = models.TextField()
    reward_hidden = models.BooleanField(default=True)



# noinspection PyTypeChecker
class Adventurer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    name = models.TextField()
    subname = models.TextField()
    in_party = models.ForeignKey(Party, on_delete=models.SET_NULL,null=True)
    origin = models.TextField()
    aclass = models.ForeignKey(AClass, on_delete=models.RESTRICT,null=True)
    race = models.ForeignKey(ARace, on_delete=models.RESTRICT,null=True)
    level = models.PositiveSmallIntegerField(default=1)
    exp = models.PositiveSmallIntegerField(default=0)
    healthcurrent = models.PositiveSmallIntegerField(default=30)
    str = models.PositiveSmallIntegerField(default=0)
    agi = models.PositiveSmallIntegerField(default=0)
    int = models.PositiveSmallIntegerField(default=0)
    spi = models.PositiveSmallIntegerField(default=0)
    cns = models.PositiveSmallIntegerField(default=0)
    cha = models.PositiveSmallIntegerField(default=0)
    luk = models.PositiveSmallIntegerField(default=0)
    free_points = models.PositiveSmallIntegerField(default=2)
    money = models.PositiveIntegerField(default=0)
    honor = models.PositiveSmallIntegerField(default=0)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_adv_for_user(sender, **kwargs):
        if kwargs.get('created'):
            print(kwargs)
            Adventurer.objects.create(user=kwargs.get('instance'))

    @property
    def weapon(self):
        return self.weapon_set()

    @property
    def armor(self):
        return self.

    @property
    def mres(self):
        return None

    @property
    def getcrit(self):
        return self.weapon.critbase if self.weapon else 0

    @property
    def getweapondamage(self):
        return self.weapon.basedamage if self.weapon else 1

    def get_calcstat(self):
        col = self.collective()
        return {
            'dmg': self.getweapondamage() * (1 + col.get('str') * .03),
            'crtd': col.get('cha') * .02,
            'crtc': col.get('agi') * 0.01 + col.get('luk') * 0.02 + self.getcrit*col.get('luk')*1.02,
            'arm': col.get('agi') * 3 + (self.armor * (1 + col.get('cha') * 0.01)),
            'mres': col.get('spi') * 3 + (self.mres * (1 + col.get('int') * 0.01)),
            'magamp': col.get('int') * 0.03 + col.get('spi') * 0.02,
            'barterbonus': col.get('int') * 0.01 + col.get('cha') * 0.02,
        }

    def addexp(self,amount):
        self.exp+=amount
        self.recalc()

    def healmax(self):
        self.healthcurrent = self.collective.get('')

    def recalc(self):
        if self.getnextlevel<0:
            atop = 0-self.getnextlevel
            self.level_up()
            self.healmax()
            self.exp=atop
            self.save()


    def level_up(self):
        self.free_points += 1
        self.save()

    def getnextlevel(self):
        return self.level*20 - self.exp


    def equipment_modifier(self,statv:str):
        return 0

    def collective(self):
        str = (self.str + (self.level * 1 * self.race.rstat== ARace.STR) + (self.level * 1 * self.aclass.sstat== AClass.STR) + (self.level * 1 * self.aclass.sstat== ARace.STR)) * self.equipment_modifier("STR")
        agi = (self.agi + (self.level * 1 * self.race.rstat== ARace.AGI) + (self.level * 1 * self.aclass.sstat== AClass.AGI) + (self.level * 1 * self.aclass.sstat== ARace.AGI)) * self.equipment_modifier("AGI")
        int = (self.int + (self.level * 1 * self.race.rstat== ARace.INT) + (self.level * 1 * self.aclass.sstat== AClass.INT) + (self.level * 1 * self.aclass.sstat== ARace.INT)) * self.equipment_modifier("INT")
        spi = (self.spi + (self.level * 1 * self.race.rstat== ARace.SPI) + (self.level * 1 * self.aclass.sstat== AClass.SPI) + (self.level * 1 * self.aclass.sstat== ARace.SPI)) * self.equipment_modifier("SPI")
        cns = (self.cns + (self.level * 1 * self.race.rstat== ARace.CNS) + (self.level * 1 * self.aclass.sstat== AClass.CNS) + (self.level * 1 * self.aclass.sstat== ARace.CNS)) * self.equipment_modifier("CNS")
        cha = (self.cha + (self.level * 1 * self.race.rstat== ARace.CHA) + (self.level * 1 * self.aclass.sstat== AClass.CHA) + (self.level * 1 * self.aclass.sstat== ARace.CHA)) * self.equipment_modifier("CHA")
        luk = (self.luk + (self.level * 1 * self.race.rstat== ARace.LUK) + (self.level * 1 * self.aclass.sstat== AClass.LUK) + (self.level * 1 * self.aclass.sstat== ARace.LUK)) * self.equipment_modifier("LUK")
        return {"str":str,"agi":agi,"int":int,"spi":spi,"cns":cns,"cha":cha,"luk":luk}


class Weapon(models.Model):
    name=models.TextField()
    description=models.TextField()
    critbase=models.PositiveSmallIntegerField()
    basedamage=models.PositiveSmallIntegerField(default=1)
    adventurer = models.ForeignKey('character.Adventurer',on_delete=models.SET_NULL,null=True)
    equipped = models.BooleanField(default=False)
    value=models.PositiveSmallIntegerField(default=5)


class BagItem(models.Model):
    adventurer = models.ForeignKey(Adventurer, on_delete=models.SET_NULL,null=True)
    name = models.TextField(default="")
    icon = models.TextField()
    quantity = models.PositiveSmallIntegerField(default=1)
    countable = models.BooleanField(default=False)
    slot = models.TextField(choices=((x,x) for x in ['head','body','armor','ring1','ring2','amulet']))
    rarity = models.TextField(choices=((x,x) for x in ['common','uncommon','rare','mythical','divine']))
    value = models.PositiveSmallIntegerField(default=0)
    equipped = models.BooleanField(default=False)

    def save(*args, **kwargs):
        super().save()

