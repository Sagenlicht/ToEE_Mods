from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Energized Shield Lesser"

def energizedShieldLesserSpellAddWeaponCondition(attachee, args, evt_obj):
    spellId = args.get_arg(0)
    elementType = args.get_arg(2)
    spellPacket = tpdp.SpellPacket(spellId)
    spellPacket.add_target(attachee, 0)
    attachee.item_condition_add_with_args('Shield Energized Lesser', elementType, 0, 0, 0, spellId)
    attachee.item_condition_add_with_args('Shield Energized Lesser Tooltip', elementType, 0, 0, 0, spellId)
    return 0

def energizedShieldLesserSpellWeaponConditionRemove(attachee, args, evt_obj):
    spellId = args.get_arg(0)
    attachee.item_condition_remove('Shield Energized Lesser', spellId)
    attachee.item_condition_remove('Shield Energized Lesser Tooltip', spellId)
    return 0

energizedShieldLesserSpell = PythonModifier("sp-Energized Shield Lesser", 4) # spell_id, duration, elementType, empty
energizedShieldLesserSpell.AddHook(ET_OnConditionAdd, EK_NONE, energizedShieldLesserSpellAddWeaponCondition,())
energizedShieldLesserSpell.AddHook(ET_OnD20PythonQuery, "PQ_Item_Buff_Duration", spell_utils.queryItemDuration, ())
energizedShieldLesserSpell.AddHook(ET_OnConditionRemove, EK_NONE, energizedShieldLesserSpellWeaponConditionRemove, ())
energizedShieldLesserSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
energizedShieldLesserSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
energizedShieldLesserSpell.AddSpellDispelCheckStandard()
energizedShieldLesserSpell.AddSpellTeleportPrepareStandard()
energizedShieldLesserSpell.AddSpellTeleportReconnectStandard()
energizedShieldLesserSpell.AddSpellCountdownStandardHook()

#### Shield Energized Lesser Condition ####

def applyParticleEffects(attachee, args, evt_obj):
    print "Debug applyParticleEffects: attachee = {}".format(attachee)
    if args.get_arg(0) == D20DT_ACID:
        spellParticles = 'sp-Resist Elements-acid'
    elif args.get_arg(0) == D20DT_COLD:
        spellParticles = 'sp-Resist Elements-cold'
    elif args.get_arg(0) == D20DT_ELECTRICITY:
        spellParticles = 'sp-Resist Elements-water'
    elif args.get_arg(0) == D20DT_FIRE:
        spellParticles = 'sp-Resist Elements-fire'
    elif args.get_arg(0) == D20DT_SONIC:
        spellParticles = 'sp-Resist Elements-sonic'
    partsysId = game.particles(spellParticles, attachee)
    args.set_arg(3, partsysId)
    return 0

def shieldEnergizedLesserOnDealingDamage(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    if spell_utils.verifyItem(usedWeapon, args):
        damageDice = dice_new('1d6') #Energized Shield Lesser adds 1d6 Bonus Damage
        damageType = args.get_arg(0)
        damageMesId = 3001 #Sonic Weapon Mess ID; needs to be changed to Energized Shield ID once Shield Bash is implemented
        evt_obj.damage_packet.add_dice(damageDice, damageType, damageMesId)
    return 0

def shieldEnergizedLesserResistEnergy(attachee, args, evt_obj):
    resistanceValue = 5 #Energized Shield Lesser grants 5 Resistance to chosen Element
    elementType = args.get_arg(0)
    damageMesId = 124 #ID 124 in damage.mes is Resistance to Energy
    evt_obj.damage_packet.add_damage_resistance(resistanceValue, elementType, damageMesId)
    return 0

def removeParticleEffects(attachee, args, evt_obj):
    game.particles_end(args.get_arg(3))
    return 0

shieldEnergizedLesser = PythonModifier("Shield Energized Lesser", 5) # elementType, empty, inventoryLocation, partsysId, spellId
shieldEnergizedLesser.AddHook(ET_OnDealingDamage, EK_NONE, shieldEnergizedLesserOnDealingDamage, ())
shieldEnergizedLesser.AddHook(ET_OnTakingDamage2, EK_NONE, shieldEnergizedLesserResistEnergy, ())
shieldEnergizedLesser.AddHook(ET_OnConditionAdd, EK_NONE, applyParticleEffects, ())
#shieldEnergizedLesser.AddHook(ET_OnConditionRemove, EK_NONE, removeParticleEffects, ())


#### Shield Energized Lesser Tooltip Condition ####

shieldEnergizedLesserToolTip = PythonModifier("Shield Energized Lesser Tooltip", 5) # elementType, empty, inventoryLocation, empty, spellId
shieldEnergizedLesserToolTip.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.itemTooltip, ())
shieldEnergizedLesserToolTip.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.itemEffectTooltip, ())