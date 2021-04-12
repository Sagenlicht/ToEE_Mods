from templeplus.pymod import PythonModifier
from toee import *
import tpdp
import tpactions
from utilities import *
print "Registering sp-Deafening Clang"

def deafeningClangSpellBonusToDamage(attachee, args, evt_obj):
    targetOfAttack = evt_obj.attack_packet.target
    spellPacket = tpdp.SpellPacket(args.get_arg(0))

    bonusDice = dice_new('1d6') #Deafening Clang Bonus Damage
    evt_obj.damage_packet.add_dice(bonusDice, D20DT_SONIC, 3004) #ID3004 added in damage.mes 

####     Deafening Part of the spell     ####
    targetIsAlreadyDeaf = targetOfAttack.d20_query(Q_Critter_Is_Deafened)
    if targetIsAlreadyDeaf:
        return 0

    #currentSequenceSpellPacket = tpactions.get_cur_seq().spell_packet
    #print "enum spell packet:", currentSequenceSpellPacket.spell_enum
    #print "currentSequence: ", currentSequenceSpellPacket
    #currentSequenceSpellPacket.spell_enum = 40
    #print "enum spell packet:", currentSequenceSpellPacket.spell_enum
    newSpellId = tpactions.get_new_spell_id()
    deafenSpellPacket = tpdp.SpellPacket(newSpellId)
    deafenSpellPacket.spell_enum = 40
    print "deafenSpellPacket Enum: ", deafenSpellPacket.spell_enum
    #tpactions.register_spell_cast(deafenSpellPacket, newSpellId)
    deafenSpellPacket.add_target(targetOfAttack, 0)
    print "Target added"
    print "Target in Registry: ", deafenSpellPacket.get_target(0)
    deafenSpellPacket.update_registry() #does not work
    if targetOfAttack.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #success
        targetOfAttack.float_mesfile_line('mes\\spell.mes', 30001)
        deafenSpellPacket.remove_target(targetOfAttack)
    else:
        targetOfAttack.float_mesfile_line('mes\\spell.mes', 30002)
        if targetOfAttack.condition_add_with_args('sp-Deafness', 0, 1, 0): #Target is deaf for 1 minute; reduced to 1 round for testing purpose
            game.particles('sp-Blindness-Deafness', targetOfAttack)
        else:
            game.particles('Fizzle', targetOfAttack)
            deafenSpellPacket.remove_target(targetOfAttack)
    if deafenSpellPacket.update_registry(): #does not work
        print "Update Registry success"
####     Deafening Part of the spell     ####
    return 0

def deafeningClangSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Deafening Clang ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Deafening Clang ({} rounds)".format(args.get_arg(1)))
    return 0

def deafeningClangSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DEAFENING_CLANG"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DEAFENING_CLANG"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def deafeningClangSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def deafeningClangSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def deafeningClangSpellSpellEnd(attachee, args, evt_obj):
    print "Deafening Clang SpellEnd"
    return 0

deafeningClangSpell = PythonModifier("sp-Deafening Clang", 4) # spell_id, duration, spellDc, hitFlag
deafeningClangSpell.AddHook(ET_OnDealingDamage, EK_NONE, deafeningClangSpellBonusToDamage,())
deafeningClangSpell.AddHook(ET_OnGetTooltip, EK_NONE, deafeningClangSpellTooltip, ())
deafeningClangSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, deafeningClangSpellEffectTooltip, ())
deafeningClangSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, deafeningClangSpellSpellEnd, ())
deafeningClangSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, deafeningClangSpellHasSpellActive, ())
deafeningClangSpell.AddHook(ET_OnD20Signal, EK_S_Killed, deafeningClangSpellKilled, ())
deafeningClangSpell.AddSpellDispelCheckStandard()
deafeningClangSpell.AddSpellTeleportPrepareStandard()
deafeningClangSpell.AddSpellTeleportReconnectStandard()
deafeningClangSpell.AddSpellCountdownStandardHook()
