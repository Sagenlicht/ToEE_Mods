from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Cloud of Bewilderment"

def cloudOfBewildermentSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    cloudOfBewildermentPartsysId = game.particles( 'sp-Cloud of Bewilderment', attachee)
    spellPacket.add_spell_object(attachee, cloudOfBewildermentPartsysId) # store the spell obj and the particle sys
    radiusCloud = 10.0
    cloudEventId = attachee.object_event_append(OLC_CRITTERS, radiusCloud)
    args.set_arg(3, cloudEventId)
    spellPacket.update_registry()
    return 0

def cloudOfBewildermentSpellOnBeginRound(attachee, args, evt_obj):
    targetsInAoe = game.obj_list_cone(attachee, OLC_CRITTERS, 10, 0, 360) #would be better to get targets from spellPacket, but it is not possible to get target list?
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    
    for cloudTarget in targetsInAoe:
        print "Target: ", cloudTarget
        queryForNausea = cloudTarget.d20_query("Nauseated Condition")
        if queryForNausea:
            return 0
        else:
            if cloudTarget.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): # save to avoid nauseated condition
                cloudTarget.float_mesfile_line('mes\\spell.mes', 30001)
            else:
                cloudTarget.condition_add_with_args('Nauseated Condition', args.get_arg(1), 0,args.get_arg(3))
    return 0

def cloudOfBewildermentSpellOnEntered(attachee, args, evt_obj):
    print "Cloud of Bewilderment enter"
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTarget = evt_obj.target
    cloudEventId = args.get_arg(3)

    if cloudEventId != evt_obj.evt_id:
        print"Mismach ID Cloud of Bewilderment"
        return 0

    if spellPacket.add_target(spellTarget, 0):
        spellTarget.condition_add_with_args('Cloud of Bewilderment Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    if spellTarget.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): # save to avoid nauseated condition
        spellTarget.float_mesfile_line('mes\\spell.mes', 30001)
    else:
        spellTarget.condition_add_with_args('Nauseated Condition', args.get_arg(1), 0, args.get_arg(3))
    return 0

def cloudOfBewildermentSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def cloudOfBewildermentSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def cloudOfBewildermentSpellSpellEnd(attachee, args, evt_obj):
    print "Cloud of BewildermentSpellEnd"
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    #spellPacket.end_target_particles(attachee) <--- does not work
    args.remove_spell_mod() #remove_spell crashes the game
    attachee.destroy()
    return 0

cloudOfBewildermentSpell = PythonModifier("sp-Cloud of Bewilderment", 4) # spell_id, duration, spellDc, eventId
cloudOfBewildermentSpell.AddHook(ET_OnConditionAdd, EK_NONE, cloudOfBewildermentSpellOnConditionAdd,())
cloudOfBewildermentSpell.AddHook(ET_OnBeginRound, EK_NONE, cloudOfBewildermentSpellOnBeginRound,())
cloudOfBewildermentSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, cloudOfBewildermentSpellOnEntered, ())
cloudOfBewildermentSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, cloudOfBewildermentSpellSpellEnd, ())
cloudOfBewildermentSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, cloudOfBewildermentSpellHasSpellActive, ())
cloudOfBewildermentSpell.AddHook(ET_OnD20Signal, EK_S_Killed, cloudOfBewildermentSpellKilled, ())
cloudOfBewildermentSpell.AddSpellDispelCheckStandard()
cloudOfBewildermentSpell.AddSpellTeleportPrepareStandard()
cloudOfBewildermentSpell.AddSpellTeleportReconnectStandard()
cloudOfBewildermentSpell.AddSpellCountdownStandardHook()

### Start Cloud Effect ###

def cloudOfBewildermentConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def cloudOfBewildermentConditionConcealment(attachee, args, evt_obj):
    evt_obj.bonus_list.add(20,0,"~Cloud of Bewilderment~[TAG_SPELLS_CLOUD_OF_BEWILDERMENT] Concealment Bonus") #Considered concealed while in Cloud of Bewilderment
    return 0

def cloudOfBewildermentConditionTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Cloud of Bewilderment (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Cloud of Bewilderment (" + str(args.get_arg(1)) + " rounds)")
    evt_obj.append("Concealed")
    return 0

def cloudOfBewildermentConditionEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CLOUD_OF_BEWILDERMENT"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("CLOUD_OF_BEWILDERMENT"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def cloudOfBewildermentConditionSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def cloudOfBewildermentConditionOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    cloudEventId = args.get_arg(3)
    if cloudEventId != evt_obj.evt_id:
        print "ID Mismach Cloud of Bewilderment"
        return 0

    args.condition_remove()
    return 0

def cloudOfBewildermentConditionOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0


cloudOfBewildermentCondition = PythonModifier("Cloud of Bewilderment Effect", 4) #spell_id, duration, spellDc, eventId
cloudOfBewildermentCondition.AddHook(ET_OnBeginRound, EK_NONE, cloudOfBewildermentConditionBeginRound, ())
cloudOfBewildermentCondition.AddHook(ET_OnGetDefenderConcealmentMissChance, EK_NONE, cloudOfBewildermentConditionConcealment, ())
cloudOfBewildermentCondition.AddHook(ET_OnGetTooltip, EK_NONE, cloudOfBewildermentConditionTooltip, ())
cloudOfBewildermentCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, cloudOfBewildermentConditionEffectTooltip, ())
cloudOfBewildermentCondition.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, cloudOfBewildermentConditionOnLeaveAoE, ())
cloudOfBewildermentCondition.AddHook(ET_OnConditionRemove, EK_NONE, cloudOfBewildermentConditionOnRemove, ())
cloudOfBewildermentCondition.AddHook(ET_OnD20Signal, EK_S_Killed, cloudOfBewildermentConditionSpellKilled, ())