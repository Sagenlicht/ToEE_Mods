from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Snipers Shot"

def snipersShotSpellAddSneakDamage(attachee, args, evt_obj):
    if args.get_arg(2): #only the first attack each round is a precision based attack
        return 0

    characterSneakDice = attachee.d20_query("Sneak Attack Dice") # get sneak dice
    targetToHit = evt_obj.attack_packet.target

    if characterSneakDice == OBJ_HANDLE_NULL: #if char has no sneak dice no damage will be added
        attachee.float_text_line("Character has no sneak attack feat!")
        return 0

##### Temporarily add Craven and Deadly Precision here #####
    if attachee.has_feat(75917982): #Craven Feat ID; not listed in constants.py, returned from print attachee.feats
        cravenFeatDamage = attachee.d20_query("Sneak Attack Bonus")
    else:
        cravenFeatDamage = 0
    if attachee.has_feat(feat_deadly_precision):
        bonusToDamageFromFeats = cravenFeatDamage + characterSneakDice
        sneakDice = dice_new('1d5+' + str(bonusToDamageFromFeats))
    else:
        sneakDice = dice_new('1d6+' + str(cravenFeatDamage))
    sneakDice.number = characterSneakDice
##### Temporarily add Craven and Deadly Precision end #####

    if not targetToHit.distance_to(attachee) > 30: #Check if out of normal Sneak Attack Range, else normal sneak attack 
        return 0

    #Check if opponent is immune to sneak attacks
    targetRacialImmunity = False
    immunityList = [mc_type_construct, mc_type_ooze, mc_type_plant, mc_type_undead]
    for critterType in immunityList:
        if targetToHit.is_category_type(critterType):
            targetRacialImmunity = True
    if targetToHit.is_category_subtype(mc_subtype_incorporeal):
        targetRacialImmunity = True
    if targetRacialImmunity:
        return 0

    # Concealment query missing

    # Target needs to either be flanked or be denied dex bonus for whatever reason to qualify for a sneak attack
    if targetToHit.d20_query(Q_Helpless) == 1 or targetToHit.d20_query(Q_Flatfooted) == 1 or (evt_obj.attack_packet.get_flags() & D20CAF_FLANKED): #does helpless include pertified and sleep?
        attachee.float_text_line("Sniper Shot") #Maybe for consistency Sneak Attack would be a better float, decided to float Sniper Shot fow now, so its clear target is more that 30 ft. away.
        evt_obj.damage_packet.add_dice(sneakDice, D20DT_UNSPECIFIED, 106) #ID106 = Sneak Damage in damage.mes 
        game.create_history_from_pattern(26, attachee, targetToHit) #ID26 = Sneak Attack in history.mes
    #args.set_arg(2, 1)
    return 0

######   Melfs Acid Arrow temporary fix   ######
def snipersShotSpellMelfsFix(attachee, args, evt_obj):
    print "Fix for Melfs"
    args.set_arg(2, 1)
    return 0
###### Melfs Acid Arrow temporary fix end ######

def snipersShotSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Snipers Shot ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Snipers Shot ({} rounds)".format(args.get_arg(1)))
    return 0

def snipersShotSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SNIPERS_SHOT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SNIPERS_SHOT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def snipersShotSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def snipersShotSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def snipersShotSpellSpellEnd(attachee, args, evt_obj):
    print "Snipers Shot SpellEnd"
    return 0

snipersShotSpell = PythonModifier("sp-Snipers Shot", 3) # spell_id, duration, notFirstAttack
snipersShotSpell.AddHook(ET_OnDealingDamage, EK_NONE, snipersShotSpellAddSneakDamage,())
snipersShotSpell.AddHook(ET_OnDealingDamageWeaponlikeSpell, EK_NONE, snipersShotSpellAddSneakDamage,())
snipersShotSpell.AddHook(ET_OnD20Signal, EK_S_EndTurn, snipersShotSpellMelfsFix, ()) #temporary Melfs Fix
snipersShotSpell.AddHook(ET_OnGetTooltip, EK_NONE, snipersShotSpellTooltip, ())
snipersShotSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, snipersShotSpellEffectTooltip, ())
snipersShotSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, snipersShotSpellSpellEnd, ())
snipersShotSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, snipersShotSpellHasSpellActive, ())
snipersShotSpell.AddHook(ET_OnD20Signal, EK_S_Killed, snipersShotSpellKilled, ())
snipersShotSpell.AddSpellDispelCheckStandard()
snipersShotSpell.AddSpellTeleportPrepareStandard()
snipersShotSpell.AddSpellTeleportReconnectStandard()
snipersShotSpell.AddSpellCountdownStandardHook()
